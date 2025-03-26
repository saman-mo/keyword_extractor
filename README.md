# ai-internal-keyword-extractor

returns insights from provided job ad: job title, skills, location and company name.

## [General Documentation](https://talentwunder.atlassian.net/wiki/spaces/DS)
- [Service Documentation](https://talentwunder.atlassian.net/wiki/spaces/DS/pages/1245053182/AI+Service+Infrastructure+Guidelines)

- [Service Code Guidelines](https://talentwunder.atlassian.net/wiki/spaces/DS/pages/1245118503/AI+Service+Implementation+Guidelines)

### Install requirements

To install the requirements, you need to provide a Personal Access Token, that is saved in the parameter store.

```bash
export ACCESS_TOKEN=<token.from.parameter.store>
pip install -r requirements.txt
```