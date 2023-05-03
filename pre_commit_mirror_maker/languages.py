from __future__ import annotations

import json
import subprocess
import urllib.request
from datetime import datetime

import packaging.version
import semver


class ReleaseDesignationUnclearError(Exception):
    pass


def semver_is_prerelease(version: str) -> bool:
    return semver.Version.parse(version).prerelease is not None


def ruby_get_package_versions(
    package_name: str, *,
    with_pre_releases: bool = False,
) -> dict[str, datetime]:
    url = f'https://rubygems.org/api/v1/versions/{package_name}.json'
    resp = json.load(urllib.request.urlopen(url))
    releases = {
        release['number']: datetime.fromisoformat(release['created_at'])
        for release in resp
        if with_pre_releases or not release['prerelease']
    }
    return dict(reversed(releases.items()))


def node_get_package_versions(
    package_name: str, *,
    with_pre_releases: bool = False,
) -> dict[str, datetime]:
    cmd = ('npm', 'view', package_name, '--json')
    output = json.loads(
        subprocess.run(
            cmd, check=True, capture_output=True, encoding='utf-8',
        ).stdout,
    )
    if not with_pre_releases:
        for release in output['versions']:
            try:
                semver.Version.parse(release)
            except ValueError as exc:
                msg = (
                    'Filtering of pre-releases was requested but '
                    f'{release} cannot be parsed as a SemVer string. '
                    'Bailing.'
                )
                raise ReleaseDesignationUnclearError(msg) from exc
    releases = {
        release: datetime.fromisoformat(output['time'][release])
        for release in output['versions']
        if with_pre_releases or not semver_is_prerelease(release)
    }
    return releases


def python_get_package_versions(
    package_name: str, *,
    with_pre_releases: bool = False,
) -> dict[str, datetime]:
    url = f'https://pypi.org/pypi/{package_name}/json'
    resp = json.load(urllib.request.urlopen(url))
    all_releases = resp['releases']
    releases = sorted(packaging.version.parse(r) for r in all_releases)
    if not with_pre_releases:
        releases = [
            release for release in releases
            if not any((release.is_prerelease, release.is_devrelease))
        ]

    def fmt_date(release: str) -> datetime:
        timestamp = all_releases[str(release)][0]['upload_time_iso_8601']
        return datetime.fromisoformat(timestamp)
    return {
        str(release):
            fmt_date(str(release))
            for release in releases
            # skip releases with no artifacts
            if len(all_releases[str(release)]) > 0
    }


def rust_get_package_versions(
    package_name: str, *,
    with_pre_releases: bool = False,
) -> dict[str, datetime]:
    url = f'https://crates.io/api/v1/crates/{package_name}'
    resp = json.load(urllib.request.urlopen(url))
    releases = {
        release['num']: datetime.fromisoformat(release['created_at'])
        for release in resp['versions']
        if with_pre_releases or not semver_is_prerelease(release['num'])
    }
    return dict(reversed(releases.items()))


def node_get_additional_dependencies(
        package_name: str, package_version: str,
) -> list[str]:
    return [f'{package_name}@{package_version}']


def rust_get_additional_dependencies(
        package_name: str, package_version: str,
) -> list[str]:
    return [f'cli:{package_name}:{package_version}']


LIST_VERSIONS = {
    'node': node_get_package_versions,
    'python': python_get_package_versions,
    'ruby': ruby_get_package_versions,
    'rust': rust_get_package_versions,
}

ADDITIONAL_DEPENDENCIES = {
    'node': node_get_additional_dependencies,
    'rust': rust_get_additional_dependencies,
}
