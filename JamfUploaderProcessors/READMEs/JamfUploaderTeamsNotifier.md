# JamfUploaderTeamsNotifier

## Description

A postprocessor for AutoPkg that will send details about a recipe run to a Microsoft Teams webhook.

## Input variables

- **JSS_URL:**
  - **required:** True
  - **description:** URL to a Jamf Pro server. Used to display which JSS server the recipe was run against.
- **POLICY_CATEGORY:**
  - **required:** False
  - **description:** Category for the created/updated policy.
- **PKG_CATEGORY:**
  - **required:** False
  - **description:** Category for the created/updated pkg.
- **NAME:**
  - **required:** True
  - **description:** Name of the application being created/updated.
- **pkg_name:**
  - **required:** False
  - **description:** File name of the pkg being uploaded.
- **policy_name:**
  - **required:** False
  - **description:** The uploaded policy name.
- **jamfpackageuploader_summary_result:**
  - **required:** False
  - **description:** Result of JamfPackageUploader.
- **jamfpolicyuploader_summary_result:**
  - **required:** False
  - **description:** Result of JamfPolicyUploader.
- **teams_webhook_url:**
  - **required:** True
  - **description:** Teams webhook URL to send the message to.
- **teams_username:**
  - **required:** False
  - **description:** Sets the displayname shown in the MessageCard in Teams. Defaults to AutoPkg.
- **teams_icon_url:**
  - **required:** False
  - **description:** Sets the icon shown in the MessageCard in Teams. Defaults to a Jamf Pro product icon. Recommended that you use a square image that is publicly reachable.
