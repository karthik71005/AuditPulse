# Phaze AI · Product Developer Take-Home

## Task

- **Role:** Product Developer (AI Products)
- **Company:** Phaze AI
- **Time limit:** 48 hours from the moment you receive this
- **Expected effort:** 8–12 focused hours. Do not burn the full 48.

---

# Why this task exists

We build AI products for businesses. The job is not "write code to spec"—it's taking a fuzzy business problem, deciding what the product should be, and shipping something a real customer could use.

This task is deliberately under-specified. Part of what we're grading is the decisions you make when nobody tells you what to do.

You are expected to use AI tools (Claude Code, Cursor, whatever you use). That's the job. We're not testing whether you can write a `for` loop from memory.

---

# The problem

Search is moving from Google to AI.

People now ask ChatGPT, Perplexity, Claude, and Google AI Overviews instead of typing keywords into a search bar.

That breaks the entire SEO industry's playbook. A business can rank #1 on Google and be completely invisible inside AI answers because AI engines choose their sources by a different set of rules—and most businesses have no idea what those rules are.

This new discipline is called **GEO** (Generative Engine Optimization), also known as:

- AEO
- LLMO
- AI SEO

Right now, almost no business knows whether they're visible in AI search.

There is no easy way to check.

That's the gap.

---

# What to build

Build a **GEO Auditor**.

A user enters a business—at minimum a website URL—and gets back an audit report that tells them:

1. **How visible they currently are in AI search**
   - A score
   - Evidence behind the score

2. **What is broken**
   - Specific findings
   - Proof
   - No generic advice

3. **What to fix**
   - Prioritized by **Impact × Effort**

That's it.

How you build it, what stack you use, and what the report looks like are entirely your choice.

---

# What to actually check — you decide

We are **not** giving you a checklist.

Figuring out what to measure **is the task**.

Nobody has agreed on what a GEO audit should contain yet. The field is about two years old.

Go research it:

- Read what's being written about AI search visibility.
- Look at what early tools in this space do.
- Test a few AI engines yourself.
- Notice what makes them cite one source over another.
- Decide what belongs in your auditor.

## Two rules

### 1. Go deep, not wide

Three checks done properly beat twelve that simply tick boxes.

A narrow tool that works beats a wide tool that half-works.

### 2. Be able to defend every check

In your README explain:

- Why each check exists
- Why you skipped other checks

"It was easy to build" is an acceptable reason if you say so honestly.

If two candidates submit completely different audit criteria, that's expected.

We're evaluating your reasoning as much as your code.

---

# The report is the product

**Read this section twice.**

The report is what we're actually evaluating.

A beautiful scraper with an ugly report scores badly.

## Requirements

### Score with visible breakdown

If you show a number, we must be able to see how it was calculated.

No magic **73/100**.

---

### Every finding needs evidence

A vague statement like:

> "Your site isn't optimized."

is worthless.

Instead:

- Name the exact page
- Show what you found
- Show what should be there instead

---

### Prioritized fixes

Order recommendations by:

**Impact × Effort**

The business owner should immediately know what to do Monday morning.

---

### Write for business owners

Not SEO consultants.

If you use jargon:

- Explain it inline.

---

### Copy-pasteable fixes

Whenever possible:

Don't just describe the fix.

Give them the exact text or code they can paste.

---

## Output format

Completely your choice:

- Web page
- PDF
- Dashboard
- Anything else you can defend

---

# What we are NOT asking for

Skip these unless you truly need them:

- Authentication
- Signup
- Billing
- User accounts
- Database
- Production deployment
  - Local run + demo video is perfectly acceptable.
  - A live link is a bonus.
- Tests
- CI
- Docker
- Mobile responsiveness
- Handling every website on the internet

Instead, make it work well for **3–5 real businesses**.

---

# Constraints

You may build it however you want.

No restrictions on:

- Language
- Framework
- Model
- APIs
- Tooling

Use AI tools freely:

- Claude Code
- Cursor
- Copilot
- etc.

Existing libraries are encouraged.

Don't hand-roll an HTML parser.

## Mocking

If something is mocked:

- Clearly label it in the code.
- Clearly label it in the README.

A clearly-labelled mock costs you nothing.

A fake result presented as real is an instant rejection.

## Questions

Questions are welcome.

It's a positive signal.

Don't wait for answers before starting.

Instead:

- Make an assumption.
- Document it in the README.
- Keep moving.

---

# Deliverables

Submit **all four**.

## 1. Code

A GitHub repository:

- Public
- OR private (they'll send an account to invite)

---

## 2. README

Include:

### How to run it

The reviewer should get it running in under **5 minutes**.

### What you built

More importantly:

- What you deliberately cut
- Why

### What's real vs mocked

Be explicit.

### What you'd build with another week

Future roadmap.

---

## 3. Three real audit reports

Run the tool against **three real businesses**.

Include:

- Real outputs
- Not screenshots of a template
- Not mocked reports

---

## 4. Loom video (3–5 minutes)

Walk through:

- The tool
- One report

No editing required.

Focus on:

- Decisions
- Tradeoffs
- Reasoning

Not just features.

---

# Submission

Reply on the same email/thread where you received the task.

**Subject line**

```
GEO Auditor — [Your Name]
```

If you can't finish everything:

Ship what works.

Be honest.

A working **40%** with a clear README beats a broken **90%**.

---

# How we score it

| Area | Weight | What earns points |
|-------|--------|------------------|
| Research & what you chose to check | 30% | You explored an unfamiliar field, identified what actually drives AI visibility, and built meaningful checks. This is the biggest factor. Surface-level checks score poorly even if implemented perfectly. |
| Report quality | 25% | Would a business owner pay for this report? Is it specific, evidenced, prioritized, and readable? |
| Product judgment | 20% | Did you cut the right things? Does this feel like it was built by someone solving a customer problem instead of completing a ticket? |
| Technical execution | 15% | Does it run? Does it handle messy real-world websites? Is the code maintainable? |
| Communication | 10% | README and Loom. Can you clearly explain and defend your decisions? |

---

# Instant rejection

- Tool only works for the demo URL
- Generic advice identical for every website
- Findings without evidence
- Mocked data presented as real
- Checks you cannot explain
- Missing the deadline without communication

---

# What gets you hired immediately

- We run it on a business you've never seen and it produces genuinely useful insights.
- You measure something we hadn't considered—and once we see it, we can't imagine the report without it.
- You aggressively cut scope and clearly justify every tradeoff.
- Your README changes how we think about the GEO problem.

---

# One last thing

The businesses that need this have no idea anything is wrong.

They believe they're fine because they rank on Google.

The value of this product is the moment the owner reads the report and realizes:

> "We have a problem."

Immediately underneath that realization should be the exact fix.

**Build for that moment.**