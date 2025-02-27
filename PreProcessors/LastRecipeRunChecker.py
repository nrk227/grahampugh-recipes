#!/usr/bin/python
#
# 2019 Graham R Pugh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for LastRecipeRunChecker class"""

import json
import os.path

from autopkglib import Processor, ProcessorError  # pylint: disable=import-error


__all__ = ["LastRecipeRunChecker"]


class LastRecipeRunChecker(Processor):
    """An AutoPkg pre-processor which reads the output from the LastRecipeRunResult processor from
    a different AutoPkg recipe, so that they can be used in the foillowing processes."""

    input_variables = {
        "recipeoverride_identifier": {
            "description": "The identifier of the recipe from which the information is required.",
            "required": True,
        },
        "cache_dir": {
            "description": "Path to the cache dir.",
            "required": False,
            "default": "~/Library/AutoPkg/Cache",
        },
        "info_file": {
            "description": ("Name of input file."),
            "required": False,
            "default": "latest_version.json",
        },
    }

    output_variables = {
        "url": {"description": ("the download URL.")},
        "version": {"description": ("The current package version.")},
        "minimum_os_version": {
            "description": ("The minimum OS version compatibility of a package.")
        },
        "license_key": {"description": ("The outputted value for license_key.")},
        "pkg_path": {"description": ("the package path.")},
        "pkg_name": {"description": ("the package name.")},
        "pkg_uploaded": {
            "description": ("whether a package was uploaded on the last run or not.")
        },
        "pkg_metadata_updated": {
            "description": (
                "whether package metadata was updated on the last run or not."
            )
        },
        "PKG_CATEGORY": {"description": ("The package category.")},
        "LAST_RUN_POLICY_NAME": {"description": ("The policy_name.")},
        "LAST_RUN_SELFSERVICE_DESCRIPTION": {
            "description": ("The self-service description.")
        },
    }

    description = __doc__

    def get_latest_recipe_run_info(self, cache_dir, identifier, info_file):
        """get information from the output files of a LastRecipeRunResult processor"""
        try:
            info_filepath = os.path.join(cache_dir, identifier, info_file)
            with open(info_filepath, "r") as fp:
                data = json.load(fp)
        except (IOError, ValueError):
            raise ProcessorError("No package or version information found")
        else:
            return data

    def main(self):
        identifier = self.env.get("recipeoverride_identifier")
        cache_dir = os.path.expanduser(self.env.get("cache_dir"))
        info_file = self.env.get("info_file")

        # make sure all the values were obtained from the file
        data = self.get_latest_recipe_run_info(cache_dir, identifier, info_file)
        self.env["version"] = data.get("version")
        self.env["minimum_os_version"] = data.get("minimum_os_version")
        self.env["license_key"] = data.get("license_key")
        self.env["pkg_name"] = data.get("pkg_name")
        self.env["pkg_uploaded"] = data.get("pkg_uploaded")
        self.env["pkg_metadata_updated"] = data.get("pkg_metadata_updated")
        if not self.env["version"] or not self.env["pkg_name"]:
            raise ProcessorError("No package or version information found")
        self.env["pkg_path"] = data["pkg_path"]
        self.env["url"] = data.get("url")
        self.env["PKG_CATEGORY"] = data.get("category")
        self.env["LAST_RUN_POLICY_NAME"] = data.get("policy_name")
        self.env["LAST_RUN_SELFSERVICE_DESCRIPTION"] = data.get(
            "self_service_description"
        )

        # make sure the package actually exists
        if not os.path.exists(self.env["pkg_path"]):
            raise ProcessorError(
                "Package does not exist: {}".format(self.env["pkg_path"])
            )

        self.output(f"Package name: {self.env['pkg_name']}")
        self.output(f"Package path: {self.env['pkg_path']}")
        self.output(f"Version: {self.env['version']}")
        self.output(f"Minimum OS version: {self.env['minimum_os_version']}")
        self.output(f"URL: {self.env['url']}")
        self.output(f"Pkg category: {self.env['PKG_CATEGORY']}")
        self.output(f"Policy name: {self.env['LAST_RUN_POLICY_NAME']}")
        self.output(
            f"Self Service Description: {self.env['LAST_RUN_SELFSERVICE_DESCRIPTION']}"
        )
        self.output(f"License Key: {self.env['license_key']}")
        self.output(f"Package uploaded: {self.env['pkg_uploaded']}")
        self.output(f"Package metadata updated: {self.env['pkg_metadata_updated']}")


if __name__ == "__main__":
    PROCESSOR = LastRecipeRunChecker()
    PROCESSOR.execute_shell()
