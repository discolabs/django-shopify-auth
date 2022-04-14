# Change Log
All notable changes to this project will be documented in this file.

## Unreleased
No unreleased changes.

## 1.2.3 - 2022-04-14

### Changed
-  Don't escape redirect_uri in iframe_redirect.html. Shopify gracefully handles HTML encoded URLs, but occasionally it doesn't.
- Update URL definitions to be compatible with Django 4.

## 1.2.2 - 2022-02-28

### Changed
-  Migrate redirect calls to App Bridge.

## 1.2.1 - 2021-11-08

### Added
- Added function allowing to get the user instance using the session token string.
- Added session_tokens app specific `context_processors`.

## 1.2.0 - 2021-08-17

### Added
- Added a way to customize user creation.
- Session Token Auth now supports App Bridge 2.


## 1.1.1 - 2021-04-16
### Changed
- Fixed session tokens DRF backend authentication return value.

## 1.1.0 - 2021-04-15
### Added
- Added support for session token auth.

## 1.0.2 - 2021-02-19
### Changed
- Add forgotten dependency and update other ones.

## 1.0.1 - 2020-12-09
### Changed
- Fix issue where `next` parameter wasn't honored when `SHOPIFY_APP_THIRD_PARTY_COOKIE_CHECK` is enabled.
### Added
- Added a middleware to accommodate changes to SameSite policy.

## 1.0.0 - 2020-12-06
### Changed
- 3rd party cookie check is now disabled by default as it doesn't pass Shopify's review check.
- Increased the token field max_length
- Updated test matrix to test only supported Django and Python versions

### Added
- Added a mixin which verifies that the current shop is authenticated and app is installed in shopify.
### Removed
- Dropped support for Django 1.x

## 0.9.1 - 2020-03-25
### Added
- Detection if third party cookies are allowed

### Removed
- Dropped support for Python 3.4

## 0.9.0 - 2019-12-22
### Added
- Support for Django 3 by removing Python 2 support

### Removed
- Dropped support for Python 2

## 0.8.2 - 2019-09-24
### Added
- Support for `return_to` redirect parameter.
- Added Django v2.1, v2.2 and v2.3 to test matrix.

### Removed
- Support for deprecated Django versions 1.x.

## 0.8.1 - 2019-07-01
### Changed
- Added support for Shopify API versioning.

## 0.8.0 - 2018-05-31
### Changed
- Added support for Django 2.0.

## 0.7.0 - 2017-11-24
### Changed
- Improved support for later Django versions

## 0.6.0 - 2017-11-07
### Removed
- Support for deprecated Django versions 1.7, 1.9
- Removed Python 3.3 from test matrix

## 0.5.0 - 2017-03-01
### Changed
- Updated authentication redirect for Chrome `postMessage` change

## 0.4.8 - 2016-11-11
### Changed
- Bugfix with items()/iteritems() dependence in `login_required` decorator

## 0.4.7 - 2016-10-19
### Added
- Django 1.10 support

### Removed
- Dependence on `six` package

## 0.4.6 - 2015-12-25
### Changed
- Fix OAuth regression

## 0.4.5 - 2015-12-23
### Changed
- Include templates in package

## 0.4.4 - 2015-12-19
### Changed
- *Actual* Django 1.9 compatibility

## 0.4.3 - 2015-12-19
### Changed
- Django 1.9 compatibility
- Better PEP8 conformity

## 0.4.2 - 2015-05-17
### Changed
- More Python 3 support

## 0.4.1 - 2015-05-17
### Changed
- Improve Python 3 support

## 0.4.0 - 2015-05-07
### Changed
- Updated ShopifyAPI dependency to v2.1.2

## 0.3.1 - 2014-12-06
### Added
- This new-format CHANGELOG, based on http://keepachangelog.com

### Changed
- AbstractShopUser.token now has a default value to allow easy resetting
- Improvements to README

## 0.3.0 - 2014-10-22
### Added
- Context processor to add common variables to templates

### Changed
- Major rewrite and update of README

## 0.2.5 - 2014-09-28
### Added
- Support for Django 1.7
- A `login_required` decorator to handle passing off Shopify authentication parameters to the login URL

### Removed
- Support for any version of Django < 1.7

### Fixed
- Numerous issues with packaging and distribution of templates

## 0.1.6 - 2014-08-25
### Fixed
- Move imports inside initialize() method so that we don’t break things on initial setup

## 0.1.5 - 2014-08-25
### Added
- Added `api` module for TastyPie-supported models
- Initialise properly
- Add dynamic `session` property to user

### Changed
- Swapped to setuptools for distribution

## 0.1.0 - 2014-04-04
### Added
- Initial package structure
- Custom models and decorators to support Shopify authentication
