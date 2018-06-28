"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function

import os.path
import subprocess  # pylint: disable=unused-import
import pytest  # pylint: disable=unused-import
import pysam

from mg_common.tool.bam_utils import bamUtils


def touch(path):
    """
    Functio to create empty test files for functions
    """
    with open(path, 'a'):
        os.utime(path, None)


@pytest.mark.code
def test_bam_copy():
    """
    Test the bam_index function code for counting all reads
    """
    touch("example.bam")
    result = bamUtils.bam_copy("example.bam", "example_out.bam")
    assert result is True
    assert os.path.isfile("example_out.bam") is True
    os.remove("example.bam")
    os.remove("example_out.bam")


@pytest.mark.code
def test_bam_copy_failed():
    """
    Test the bam_index function code for counting all reads
    """
    result = bamUtils.bam_copy("example.bam", "example_out.bam")
    assert result is False


@pytest.mark.code
def test_bam_count_reads(mocker):
    """
    Test the bam_index function code for counting all reads
    """
    mocker.patch('pysam.view')
    bamUtils.bam_count_reads('example.bam')
    pysam.view.assert_called_once_with(  # pylint: disable=no-member
        "-c", "example.bam")


@pytest.mark.code
def test_bam_count_reads_aligned(mocker):
    """
    Test the bam_count_reads function code for counting aligned reads
    """
    mocker.patch('pysam.view')
    bamUtils.bam_count_reads('example.bam', True)
    pysam.view.assert_called_once_with(  # pylint: disable=no-member
        "-c", "-F", "260", "example.bam")


@pytest.mark.code
def test_bam_filter(mocker):
    """
    Test the bam_filter function code
    """
    mocker.patch("subprocess.Popen")

    filter_list = {
        "duplicate": "1024",
        "unmapped": "260"
    }

    for filter_name in filter_list:
        # Using samtools directly as pysam.view ignored the '-o' parameter
        cmd_view = ' '.join([
            "samtools view",
            "-b",
            "-F", filter_list[filter_name],
            "-o", "example.filtered.bam",
            "example.bam"
        ])

        result = bamUtils.bam_filter("example.bam", "example.filtered.bam", filter_name)
        subprocess.Popen.assert_called_with(cmd_view, shell=True)  # pylint: disable=no-member
        assert result is True

    # os.remove("example.filtered.bam")


@pytest.mark.code
def test_bam_index(mocker):
    """
    Test the bam_index function code
    """
    touch("example.bam")
    touch("example.bam_tmp.bai")
    touch("example.bam.bai")

    cmd_view = " ".join([
        "samtools index",
        "-b",
        "example.bam",
        "example.bam_tmp.bai"
    ])
    mocker.patch("subprocess.Popen")

    result = bamUtils.bam_index("example.bam", "example.bam.bai")
    subprocess.Popen.assert_called_once_with(cmd_view, shell=True)  # pylint: disable=no-member
    assert result is True

    os.remove("example.bam")
    os.remove("example.bam_tmp.bai")
    os.remove("example.bam.bai")


@pytest.mark.code
def test_bam_merge_list(mocker):
    """
    Test the bam_merge list function code
    """
    mocker.patch('pysam.merge')
    result = bamUtils.bam_merge(['example_1.bam', 'example_2.bam'])
    pysam.merge.assert_called_once_with(  # pylint: disable=no-member
        '-f', 'example_1.bam_merge.bam', 'example_1.bam', 'example_2.bam')
    assert result is False


@pytest.mark.code
def test_bam_merge(mocker):
    """
    Test the bam_merge function code
    """
    mocker.patch('pysam.merge')
    result = bamUtils.bam_merge('example_1.bam', 'example_2.bam')
    pysam.merge.assert_called_once_with(  # pylint: disable=no-member
        '-f', 'example_1.bam_merge.bam', 'example_1.bam', 'example_2.bam')
    assert result is False


@pytest.mark.code
def test_bam_list_chromosomes(mocker):
    """
    Test the bam_list_chromosome function code
    """
    mocker.patch('pysam.AlignmentFile')
    result = bamUtils.bam_list_chromosomes("example.bam")
    pysam.AlignmentFile.assert_called_once_with("example.bam", "rb")  # pylint: disable=no-member
    assert isinstance(result, list) is True


@pytest.mark.code
def test_bam_sort(mocker):
    """
    Test the bam_sort function code
    """
    mocker.patch('pysam.sort')
    result = bamUtils.bam_sort('example.bam')
    pysam.sort.assert_called_once_with(  # pylint: disable=no-member
        '-o', 'example.bam', '-T', 'example.bam' + '_sort', 'example.bam')
    assert result is True


@pytest.mark.code
def test_bam_split(mocker):
    """
    Test the bam_filter function code
    """
    mocker.patch("subprocess.Popen")

    touch("example.bam")
    touch("example.bai")
    touch("example.I.bam")
    touch("example.bam.sam")

    cmd_view_1 = ' '.join([
        'samtools view',
        '-h',
        '-o', "example.bam.sam",
        "example.bam",
        "I"
    ])

    mocker.patch("mg_common.tool.bam_utils.bamUtils.sam_to_bam")

    result = bamUtils.bam_split("example.bam", "example.bai", "I", "example.I.bam")
    subprocess.Popen.assert_called_with(cmd_view_1, shell=True)  # pylint: disable=no-member
    assert result is True

    os.remove("example.bam")
    os.remove("example.bai")
    os.remove("example.I.bam")


@pytest.mark.code
def test_sam_to_bam(mocker):
    """
    Test the bam_filter function code
    """
    mocker.patch("subprocess.Popen")

    touch("example.bam.sam")

    cmd_sort = ' '.join([
        'samtools sort',
        '-O bam',
        '-o', "example.bam",
        "example.bam.sam"
    ])

    mocker.patch("subprocess.Popen")

    result = bamUtils.sam_to_bam("example.bam.sam", "example.bam")
    subprocess.Popen.assert_called_with(cmd_sort, shell=True)  # pylint: disable=no-member
    assert result is True

    os.remove("example.bam.sam")
