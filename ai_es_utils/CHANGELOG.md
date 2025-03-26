# Changelog

## [4.3.0](https://github.com/Talentwunder/ai-es-utils/compare/v4.2.1...v4.3.0) (2022-12-21)


### Features

* add distance query based on provided geo coordiantes ([328d6f1](https://github.com/Talentwunder/ai-es-utils/commit/328d6f1303a51836e2ec66559e077abb05563802))

## [4.2.1](https://github.com/Talentwunder/ai-es-utils/compare/v4.2.0...v4.2.1) (2022-11-01)


### Bug Fixes

* add missing bearer_token kwarg to new job2jobs and job2skills client call ([547d6a5](https://github.com/Talentwunder/ai-es-utils/commit/547d6a56165225d21af1476849c70bbea24b1c44))

## [4.2.0](https://github.com/Talentwunder/ai-es-utils/compare/v4.1.1...v4.2.0) (2022-11-01)


### Features

* add new job2jobs and job2skills clients for internal endpoints ([3687da9](https://github.com/Talentwunder/ai-es-utils/commit/3687da90527a92989f4debb619f66f77f7664255))

## [4.1.1](https://github.com/Talentwunder/ai-es-utils/compare/v4.1.0...v4.1.1) (2022-11-01)


### Bug Fixes

* modifying Photon api to accept additional kwargs ([d8c2197](https://github.com/Talentwunder/ai-es-utils/commit/d8c2197bd2b4c9f5f5e073468c95bc16b30ef3ef))

## [4.1.0](https://github.com/Talentwunder/ai-es-utils/compare/v4.0.2...v4.1.0) (2022-10-20)


### Features

* implement alternative geolocation serivce using photon api ([7c9cb89](https://github.com/Talentwunder/ai-es-utils/commit/7c9cb89c4024b23d1ccf2f8afab4ecd0935446d0))

## [4.0.2](https://github.com/Talentwunder/ai-es-utils/compare/v4.0.1...v4.0.2) (2022-09-16)


### Bug Fixes

* DATA-401 - Issue with specific countries' codes due to size and underscore chars in the Autocompletion list ([120805f](https://github.com/Talentwunder/ai-es-utils/commit/120805f24238719d868ef39d0795878ee4f41fb4))

## [4.0.1](https://github.com/Talentwunder/ai-es-utils/compare/v4.0.0...v4.0.1) (2022-09-15)


### Bug Fixes

* Edited the country RegEx to solve issue with USA country queries ([3bb566d](https://github.com/Talentwunder/ai-es-utils/commit/3bb566da985a67cc3c6436553dbd0e8477aed9c8))

## [4.0.0](https://github.com/Talentwunder/ai-es-utils/compare/v3.2.1...v4.0.0) (2022-08-25)


### ⚠ BREAKING CHANGES

* update code to elasticsearch v8 and new authorization requirement (using api_key)
* remove discontinued elasticsearch_dsl dependency

### Features

* update code to elasticsearch v8 and new authorization requirement (using api_key) ([847613b](https://github.com/Talentwunder/ai-es-utils/commit/847613b9ff1646bc03576b32269c218c08db873e))


### Bug Fixes

* remove discontinued elasticsearch_dsl dependency ([5225e2d](https://github.com/Talentwunder/ai-es-utils/commit/5225e2d6112eb0dfb27d6e0d2311a30e6aaa79a1))

## [3.2.1](https://github.com/Talentwunder/ai-es-utils/compare/v3.2.0...v3.2.1) (2022-08-11)


### Bug Fixes

* revert unintended change to elasticsearch service endpoint handling ([a9ae22c](https://github.com/Talentwunder/ai-es-utils/commit/a9ae22c8554a5f2a08cd43dfe7b0f45ecb101cce))

## [3.2.0](https://github.com/Talentwunder/ai-es-utils/compare/v3.1.2...v3.2.0) (2022-08-10)


### Features

* add release-please workflow Talentwunder/DATA-322/add-release-please-workflow ([4cf28e3](https://github.com/Talentwunder/ai-es-utils/commit/4cf28e3e3560e945d3f8fb48b0f59caf16240753))
