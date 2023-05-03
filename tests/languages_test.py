from __future__ import annotations

from pre_commit_mirror_maker.languages import node_get_package_versions
from pre_commit_mirror_maker.languages import python_get_package_versions
from pre_commit_mirror_maker.languages import ruby_get_package_versions
from pre_commit_mirror_maker.languages import rust_get_package_versions


def assert_all_text(versions):
    for version in versions:
        assert type(version) is str


def test_node_get_package_version_output():
    ret = node_get_package_versions('jshint')
    assert ret
    assert_all_text(ret)


def test_node_get_package_version_output_with_pre_releases():
    ret = node_get_package_versions('jshint', with_pre_releases=True)
    assert ret
    assert '2.13.4' in ret
    assert '2.11.0-rc1' in ret


def test_node_get_package_version_output_without_pre_releases():
    ret = node_get_package_versions('jshint', with_pre_releases=False)
    assert ret
    assert '2.13.4' in ret
    assert '2.11.0-rc1' not in ret


def test_python_get_package_version_output():
    ret = python_get_package_versions('flake8')
    assert ret
    assert_all_text(ret)


def test_python_get_package_version_output_with_pre_releases():
    ret = python_get_package_versions('flake8', with_pre_releases=True)
    assert ret
    assert '3.7.9' in ret
    assert '3.8.0a2' in ret


def test_python_get_package_version_output_without_pre_releases():
    ret = python_get_package_versions('flake8', with_pre_releases=False)
    assert ret
    assert '3.7.9' in ret
    assert '3.8.0a2' not in ret


def test_ruby_get_package_version_output():
    ret = ruby_get_package_versions('puppet-lint')
    assert ret
    assert_all_text(ret)


def test_ruby_get_package_version_output_with_pre_releases():
    ret = ruby_get_package_versions('puppet-lint', with_pre_releases=True)
    assert ret
    assert '3.4.0' in ret
    assert '4.0.0.rc.1' in ret


def test_ruby_get_package_version_output_without_pre_releases():
    ret = ruby_get_package_versions('puppet-lint', with_pre_releases=False)
    assert ret
    assert '3.4.0' in ret
    assert '4.0.0.rc.1' not in ret


def test_rust_get_package_version_output():
    ret = rust_get_package_versions('clap')
    assert ret
    assert_all_text(ret)


def test_rust_get_package_version_output_with_pre_releases():
    ret = rust_get_package_versions('clap', with_pre_releases=True)
    assert ret
    assert '4.2.3' in ret
    assert '4.0.0-rc.3' in ret


def test_rust_get_package_version_output_without_pre_releases():
    ret = rust_get_package_versions('clap', with_pre_releases=False)
    assert ret
    assert '4.2.3' in ret
    assert '4.0.0-rc.3' not in ret
