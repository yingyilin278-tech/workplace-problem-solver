# Security and privacy policy

## Supported version

Security and privacy fixes target the latest commit on the default branch.

## Reporting

Do not disclose credentials, personal data or exploitable details in a public Issue. Contact the repository maintainer through the private security-reporting channel available on the GitHub repository.

Include:

- affected file or script;
- impact and reproduction conditions;
- whether personal data, credentials or external network access are involved;
- the smallest safe reproduction example.

## Threat model

Review contributions for:

- prompt injection hidden in source material;
- scripts that execute commands or access the network unexpectedly;
- credential or cookie collection;
- path traversal and unsafe file writes;
- publication of private or copyrighted source material;
- advice that presents guesses as facts or oversteps legal, medical or safety boundaries.

Never run newly contributed scripts on confidential files before reviewing their code and dependencies.

