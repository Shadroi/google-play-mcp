# Google Play Developer API MCP Server

A Model Context Protocol (MCP) server for managing Google Play app deployment and in-app products via the Android Publisher API v3.

## Features

### App Deployment

- **deploy_internal**: Upload AAB and deploy to internal testing track
- **deploy_track**: Upload AAB and deploy to any supported track
- **promote_track_release**: Promote an existing uploaded release between tracks without re-uploading an AAB

### In-App Products

- **create_inapp_product**: Create or update a single in-app product
- **batch_create_inapp_products**: Create multiple products at once
- **activate_inapp_product**: Activate a draft product
- **batch_activate_inapp_products**: Activate multiple products
- **deactivate_inapp_product**: Deactivate an active product
- **list_inapp_products**: List all one-time products
- **create_subscription_product**: Create or update a subscription product
- **list_subscriptions**: List all subscription products

### App Info

- **get_app_info**: Get app track and version information

## Requirements

- Python 3.10+
- Google Cloud service account with Google Play Developer API access
- App registered in Google Play Console

## Installation & Usage

You can use this MCP server directly with `npx` without installing it manually.

### Quick Start (npx)

```bash
# Configure your API key
npx google-play-mcp init-key

# For Korean instructions (한국어 안내)
npx google-play-mcp init-key --lang ko

# Start the server
npx google-play-mcp start
```

### Installation (Global)

If you prefer to install it globally (from npm):

```bash
npm install -g google-play-mcp
```

### Installation (Local Dev)

To install from the cloned repository:

```bash
npm install -g .
```

Then you can run:

```bash
google-play-mcp init-key
google-play-mcp start
```

## Configuration (Antigravity & Claude Desktop)

To use this MCP server, add the following configuration to your MCP client (e.g., `claude_desktop_config.json` or Antigravity settings):

```json
{
  "mcpServers": {
    "google-play": {
      "command": "google-play-mcp",
      "args": ["start"],
      "env": {
        "GOOGLE_PLAY_KEY_FILE": "/absolute/path/to/your-key.json",
        "GOOGLE_PLAY_PACKAGE_NAME": "com.yourcompany.yourapp"
      }
    }
  }
}
```

> **Note:** If you haven't run `init-key` or don't have a `.env` file, you can pass environment variables directly in the configuration as shown above. If you have a `.env` file in the working directory, the server will load it automatically.

## Configuration (Codex)

If your workspace layout is:

```
/Users/<you>/Foreign-Language-Battle/
  └─ google-play-mcp/
```

you can run this MCP server from the cloned repository directory.

1. Create `.env` inside `google-play-mcp`:

```bash
cd /Users/<you>/Foreign-Language-Battle/google-play-mcp
cp .env.example .env
# edit .env and set:
# GOOGLE_PLAY_KEY_FILE=/absolute/path/to/service-account.json
# GOOGLE_PLAY_PACKAGE_NAME=com.yourcompany.yourapp
```

2. Install dependencies:

```bash
cd /Users/<you>/Foreign-Language-Battle/google-play-mcp
pip install -r requirements.txt
```

3. Add MCP server entry in Codex config (example):

```json
{
  "mcpServers": {
    "google-play": {
      "command": "python3",
      "args": ["server.py"],
      "cwd": "/Users/<you>/Foreign-Language-Battle/google-play-mcp",
      "env": {
        "GOOGLE_PLAY_KEY_FILE": "/absolute/path/to/service-account.json",
        "GOOGLE_PLAY_PACKAGE_NAME": "com.yourcompany.yourapp"
      }
    }
  }
}
```

4. Restart Codex (or reload MCP servers), then call tools such as
`get_app_info`, `create_inapp_product`, and `create_subscription_product`.

1. Login to npm:

```bash
npm login
```

1. Publish the package:

```bash
npm publish
```

## Configuration

The `npm run init-key` script will automatically create a `.env` file with your configuration:

```
GOOGLE_PLAY_KEY_FILE=/absolute/path/to/your-key.json
GOOGLE_PLAY_PACKAGE_NAME=com.yourcompany.yourapp
```

## Usage

To start the server manually:

```bash
npm start
```

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-play": {
      "command": "npm",
      "args": ["start"],
      "cwd": "/absolute/path/to/google-play-mcp"
    }
  }
}
```

## Tool Examples

### Deploy to Internal Testing

```
Deploy app-release.aab to internal testing with Korean and English release notes
```

### Promote Internal Release to Production

```
Promote the existing internal track release to production without uploading a new AAB.
Set Korean release notes to 버그 핫픽스 and English release notes to Bug hotfix.
```

### Create In-App Product

```
Create an in-app product:
- SKU: gems_100
- Korean: 보석 100개 / 보석 100개를 획득합니다
- English: 100 Gems / Get 100 gems
- Price: $0.99 USD
```

### Batch Create Products

```json
[
  {"sku": "gems_12", "title_ko": "보석 12개", "title_en": "12 Gems",
   "description_ko": "보석 12개 획득", "description_en": "Get 12 gems", "price_usd": 0.99},
  {"sku": "gems_66", "title_ko": "보석 66개", "title_en": "66 Gems",
   "description_ko": "보석 66개 획득", "description_en": "Get 66 gems", "price_usd": 4.99}
]
```

### Activate Products

```json
["gems_12", "gems_66", "gems_136"]
```

### Create Subscription Product

```
Create a subscription product:
- Product ID: malto_plus_monthly
- Base Plan ID: monthly
- Korean: 말투 플러스 월간 / 매일 보석을 지급하는 월간 구독
- English: Malto Plus Monthly / Monthly subscription with daily gem rewards
- Price: $4.99 USD
- Billing Period: P1M
```

## Important Notes

### Prerequisites for In-App Products

Before creating in-app products, your app must have:

1. `com.android.vending.BILLING` permission in `AndroidManifest.xml`
2. Play Billing Library 6.0.1+ (Flutter: `in_app_purchase` package)
3. A bundle with these uploaded to Google Play

### Draft Apps

Apps that have never been published can only use `status: "draft"` for deployments.
You must manually publish through Google Play Console for the first release.

### API Migration

This server uses the new `monetization.onetimeproducts` API instead of the deprecated
`inappproducts` API which returns 403 errors.

### Price Conversion

USD prices are automatically converted to 170+ regional currencies using
Google's `convertRegionPrices` API.

## Tracks

| Track | Description |
|-------|-------------|
| `internal` | Internal testing (up to 100 testers) |
| `alpha` | Closed testing |
| `beta` | Open testing |
| `production` | Production release |

## License

MIT License
