# merit-demo — standard usage 🧭

This is the public demo people use to see MERIT in action. You do not need to run a server, create a cloud account, or understand the files behind the scenes to follow this guide.

## Quick index

- [The standard three-part journey](#the-standard-three-part-journey)
- [What you should see](#what-you-should-see)
- [Publish and tour your hosted app](#publish-and-tour-your-hosted-app)
- [Hosted creator path](#hosted-creator-path)
- [Advanced reference](#advanced-reference)

<a id="the-standard-three-part-journey"></a>
## The standard three-part journey 🍽️

### 1. Start — prepare the laptop

- Download and run [Merit-Hub.ps1](https://github.com/AgentDraven/merit-agent-skills/blob/main/Merit-Hub/Merit-Hub.ps1) from a tools folder.
- Choose **Set up this laptop (1)**, then **Get the free MERIT tools (2)**.
- Choose **Try it (3)**. The Hub downloads or refreshes this demo, starts its local web page, and opens it for you.

### 2. Make progress — look around

- Open the `/play/` page and read the **Hello, meritutils** message.
- Check for **Hosted Ready** and the mounted workbench.
- Try the guest controls, navigation, and **Register free** link. This is a visitor tour; no account is required.

### 3. Finish — prove what you saw

- Choose **Validate my local demo (3V)** in the Hub whenever you want the guided check again.
- Confirm the play page, workbench, registration link, and local marketing page behave as described.
- Save the receipt or a screenshot if you want a record. You can repeat the journey whenever you like.

<a id="what-you-should-see"></a>
## What you should see ✅

Step 3 is a thin demonstration, not a second copy of the MERIT cloud. The page shell and marketing text run on your laptop; the shared workbench package and MERIT services are loaded from the production package host.

The Hub starts or reuses local HTTP port `3000` and records its server note in the evidence folder. If a hosted package cannot load, the page shows a clear offline message with retry guidance—not an endless spinner and not a pretend local replacement.

The demo has separate visitor pages for the home page, play, journal, AMA, legal information, and the marketing portal. The free package and registration links are shared MERIT services; your consumer page remains its own app surface.

<a id="publish-and-tour-your-hosted-app"></a>
## Publish and tour your hosted app ☁️

After the local journey and **3V** check succeed:

1. Choose **OSS in Cloud (OC)** in the Hub.
   - The Hub checks the demo files and the MERIT host.
   - It creates or uses your consumer identity.
   - It prints hosted play, free registration, and marketing links.
2. Choose **Walk through my hosted demo (OCV)**.
   - Open each printed link one at a time.
   - Check the page title, welcome message, controls, and registration route.
   - Keep the OC receipt if you need to report a problem.

OC does not require a Vercel, Supabase, Square, or here.now account. Those are optional services for people who deliberately want to run their own infrastructure.

<a id="hosted-creator-path"></a>
## Hosted creator path 🌱

Creators, affiliates, and design partners can stay on the managed MERIT path:

1. **Start — tell MERIT what you want to share.**
   - Use the hosted partner page or your MERIT invitation.
   - Choose a name and the audience you want to help.
   - Keep your first version on the OC-hosted consumer surface.
2. **Make progress — shape the experience.**
   - Update your welcome words, branding, and visitor story.
   - Use OC to publish your consumer-specific play, registration, and marketing pages.
   - Let MERIT manage the shared hosting, registration, and usage rails.
3. **Finish — invite people.**
   - Share the hosted links printed by OC.
   - Visitors can try the free experience before choosing to register.
   - If paid features are enabled later, onboarding explains fees, creator share, and payout requirements.

## Standard checks

The normal Hub journey is enough. If you want to repeat it from the demo folder, use the helper the Hub installed:

```powershell
.\merit.ps1 verify
```

The check confirms the built pages, hosted package references, visitor routes, and registration link. Use the Hub’s **3V** menu entry for the same checks with a guided explanation.

<a id="advanced-reference"></a>
## Advanced reference 🔧

<details>
<summary>Open only when you deliberately want engineering, screenshots, or your own cloud services</summary>

### Your own services (optional)

Use [OPERATOR_PROVISION.md](OPERATOR_PROVISION.md) only when you deliberately want your own Vercel deployment, Supabase database, payment-provider relationship, or here.now marketing host. It contains account setup, environment values, migrations, and deployment work that the hosted OC path avoids.

### Command-line build and deployment

The public helper can run deeper checks when an experienced builder requests them:

```powershell
.\merit.ps1 verify
.\merit.ps1 e2e
.\merit.ps1 closeout
```

These commands are not needed for the standard Hub tour. Public creators should use the Hub and `verify`; operators can use the advanced checklist for their own deployment.

### Optional picture checks

If you want screenshots of every visitor page, let the MERIT helper prepare and run its picture check:

```powershell
.\merit.ps1 e2e:playwright
```

When the optional browser tools are available, the helper opens a temporary browser and saves the pictures under `merit-demo docs/evidence/`. If they are unavailable or the check fails, nothing is wrong with the standard path. Return to the Hub and choose **3V**.

### Local service boundary

The public demo does not ship a local billing or usage-metering service. Its workbench and shared provider references point to MERIT-hosted services. Your own persistent journal/AMA database is only needed for a deliberate self-hosted deployment.

### Evidence

When the optional picture check is installed, screenshots are written under `merit-demo docs/evidence/`. They are supporting evidence for maintainers, not a requirement for trying the demo.

</details>

## When to move beyond the standard path

Stay with OC while it gives you the managed experience you want. Consider the advanced operator route only when you need to own infrastructure, data storage, payment-provider configuration, or a separate deployment policy. The hosted path remains the recommended way to learn, share, and grow.
