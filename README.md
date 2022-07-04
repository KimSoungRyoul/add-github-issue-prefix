# add-github-issue-prefix-hook

for people who always said "oh I forgot to prefix msg"

### [pre-commit hook] 

this hook are made to contain prefix github issue

#### branch -> commit msg prefix
* feat/#111  -> [#111]
* feature/#111  -> [#111]
* fix/#111-hello-branch -> [#111]
* chore/#111-run-autoflake -> [#111]


## 1. Quick Start

0. `brew install pre-commit`

1. create file to Repository Root Path `.pre-commit-config.yaml`

2. copy & paste
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/KimSoungRyoul/add-github-issue-prefix
      rev: v1.0.4
      hooks:
        - id: add-github-issue-prefix
```

3. install hook ( script is created under the `.git/hooks` )
```
pre-commit install --hook-type prepare-commit-msg
```

## 2. Customize


```yaml
-   repo: https://github.com/KimSoungRyoul/add-github-issue-prefix
    rev: v1.0.4
    hooks:
    -   id: add-github-issue-prefix
        args:
            - --template=[{}] # default: [{}]
            - --regex='#\d{1,5}' # default: #\d{1,5}"

```
