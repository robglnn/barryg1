# GitHub Setup with Personal Access Token

## Quick Setup

Your repository is configured to use HTTPS authentication with a personal access token.

## Token Storage (macOS)

To avoid entering the token every time, you can store it in the macOS Keychain:

```bash
# Store credentials in macOS Keychain
git config --global credential.helper osxkeychain

# When you push, enter:
# Username: robglnn
# Password: <your personal access token>
```

The token will be stored securely in your macOS Keychain.

## Alternative: Use Token in URL (Temporary)

For a one-time push, you can embed the token in the URL:

```bash
git remote set-url origin https://robglnn:YOUR_TOKEN@github.com/robglnn/barryg1.git
git push -u origin main
```

**⚠️ Security Note:** Remove the token from the URL after pushing:
```bash
git remote set-url origin https://github.com/robglnn/barryg1.git
```

## Your Token

**⚠️ Important Security Notes:**
- **NEVER commit tokens to git** - They are in `.gitignore` but always double-check
- Store tokens securely using macOS Keychain (see above)
- If a token is exposed, **revoke it immediately** at: https://github.com/settings/tokens
- Personal access tokens start with: `ghp_`, `ghs_`, `gho_`, `ghu_`, or `ghr_`
- All token patterns are automatically ignored by `.gitignore`

## Repository URL

- **HTTPS**: https://github.com/robglnn/barryg1.git
- **SSH**: git@github.com:robglnn/barryg1.git (requires SSH key setup)

