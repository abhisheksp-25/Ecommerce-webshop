app_name = "e_commerce_application"
app_title = "E Commerce Application"
app_publisher = "abhishekspatil90@gmail.com"
app_description = "E Commerce Application"
app_email = "abhishekspatil90@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "e_commerce_application",
# 		"logo": "/assets/e_commerce_application/logo.png",
# 		"title": "E Commerce Application",
# 		"route": "/e_commerce_application",
# 		"has_permission": "e_commerce_application.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/e_commerce_application/css/e_commerce_application.css"
# app_include_js = "/assets/e_commerce_application/js/e_commerce_application.js"

# include js, css files in header of web template
# web_include_css = "/assets/e_commerce_application/css/e_commerce_application.css"
# web_include_js = "/assets/e_commerce_application/js/e_commerce_application.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "e_commerce_application/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "e_commerce_application/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "e_commerce_application.utils.jinja_methods",
# 	"filters": "e_commerce_application.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "e_commerce_application.install.before_install"
# after_install = "e_commerce_application.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "e_commerce_application.uninstall.before_uninstall"
# after_uninstall = "e_commerce_application.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "e_commerce_application.utils.before_app_install"
# after_app_install = "e_commerce_application.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "e_commerce_application.utils.before_app_uninstall"
# after_app_uninstall = "e_commerce_application.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "e_commerce_application.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"e_commerce_application.tasks.all"
# 	],
# 	"daily": [
# 		"e_commerce_application.tasks.daily"
# 	],
# 	"hourly": [
# 		"e_commerce_application.tasks.hourly"
# 	],
# 	"weekly": [
# 		"e_commerce_application.tasks.weekly"
# 	],
# 	"monthly": [
# 		"e_commerce_application.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "e_commerce_application.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "e_commerce_application.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "e_commerce_application.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["e_commerce_application.utils.before_request"]
# after_request = ["e_commerce_application.utils.after_request"]

# Job Events
# ----------
# before_job = ["e_commerce_application.utils.before_job"]
# after_job = ["e_commerce_application.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"e_commerce_application.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

doc_events = {
    "Employee": {
        "validate": "e_commerce_application.e_commerce_application.custom_scripts.employee.employee.validate",
        "on_update": "e_commerce_application.e_commerce_application.custom_scripts.employee.employee.after_save",
    },
    
    "Task": {
        "validate": "e_commerce_application.e_commerce_application.custom_scripts.task.task.validate"
    },

    
    "User": {
        "after_insert": "e_commerce_application.e_commerce_application.custom_scripts.user.user.after_insert"
    },

    "Quotation": {
        "on_submit":"e_commerce_application.e_commerce_application.custom_scripts.quotation.quotation.create_sales_order"
    },


    "Address": {
        "validate": "e_commerce_application.e_commerce_application.custom_scripts.address.address.validate"
    },

    "Sales Order": {
    "before_insert": "e_commerce_application.e_commerce_application.custom_scripts.sales_order.sales_order.assign_supplier",
    "on_submit": "e_commerce_application.e_commerce_application.custom_scripts.sales_order.sales_order.create_delivery_note"
    },

    "Delivery Note": {
        "on_submit": "e_commerce_application.e_commerce_application.custom_scripts.delivery_note.delivery_note.create_sales_invoice"
    },

    "Sales Invoice": {
        "on_submit": "e_commerce_application.e_commerce_application.custom_scripts.sales_invoice.sales_invoice.create_payment_entry"
    },

    "Supplier Inquiry": {
        "after_insert": "e_commerce_application.e_commerce_application.custom_scripts.supplier.supplier_inquiry.process_new_inquiry",
    },

    "Supplier Registration": {
    "before_insert": "e_commerce_application.e_commerce_application.custom_scripts.supplier.supplier_registration.validate_registration_token",
    "after_insert": "e_commerce_application.e_commerce_application.custom_scripts.supplier.supplier_registration.mark_token_consumed",
    }

}


doctype_js = {
    "Employee": "public/js/employee.js"
}

