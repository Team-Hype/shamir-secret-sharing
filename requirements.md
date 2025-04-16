## Implement Shamir secret sharing algorithm: for sharing a secret among a group.
 * Read the [original paper](https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf) and check the [visualization](https://iancoleman.io/shamir/)
 * Implement the scheme to share a text secret, with a web UI for demo. 
### Validation Checklist:
 - [ ] Hash the input and reconstructed secrets to confirm integrity
 - [ ] Attempt reconstruction with insufficient shares (should fail)
 - [ ] Log generation and reconstruction steps for auditability
