# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A minimal Jenkins pipeline project. The `Jenkinsfile` at the repo root is the entire pipeline definition — there is no application code, no build tooling, and no dependency manifest here.

## Running the pipeline

There is no local build/test/lint command — the `Jenkinsfile` only runs when executed by Jenkins.

- Jenkins runs on the same Windows machine as a Windows service (`Get-Service Jenkins`), listening on `http://localhost:8080`.
- The service's startup type is **Manual** (auto-start on boot was intentionally disabled) — it must be started before use.
- Use `python jenkins_ctl.py {start|stop|status}` (in this folder) to control it. `start`/`stop` trigger a UAC prompt (admin required to control a Windows service); `status` does not. `start` also polls `http://localhost:8080` until Jenkins actually responds, since the JVM takes ~10-15s to boot after the service reports running.
- The Jenkins job is named `basic-pipeline`, configured as **Pipeline script from SCM** pointing at this repo's GitHub remote (`origin`, `main` branch), with Script Path `Jenkinsfile`.
- To run it: ensure Jenkins is started (see above), push changes to `main` on GitHub, then trigger a build from the Jenkins UI (**Build Now** on the `basic-pipeline` job) — there is no webhook configured yet, so builds are manual.
- The repo must stay public (or the Jenkins job needs a credential configured) — Jenkins runs as the `LocalSystem` account with no interactive login, so it cannot use cached/interactive git credentials for a private remote.

## Architecture

The pipeline is a single declarative `Jenkinsfile` with `agent any` and three sequential stages (`Build`, `Test`, `Deploy`), each currently a placeholder `bat` step. Steps use `bat` (not `sh`) because the Jenkins agent is Windows.

When adding real steps, keep in mind the execution environment is Windows batch, not a POSIX shell.
