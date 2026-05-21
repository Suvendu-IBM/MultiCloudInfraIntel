# Prompt: Context Studio Setup Guide

## Context
This prompt was used to create a comprehensive setup guide for configuring Context Studio with the JSON-LD schema and policy markdown files, enabling AI agents to understand and enforce policies.

## Original Prompt to Bob

Bob, create a detailed setup guide for Context Studio that explains how to configure the JSON-LD schema, link policy markdown files, and enable AI agents to understand the semantic model.

## Setup Requirements

### Context Studio Configuration

**Components to Configure:**
1. **JSON-LD Schema Import** - Import `schema/policies.jsonld`
2. **Policy Markdown Linking** - Link 8 policy markdown files
3. **Entity Relationships** - Configure entity relationships
4. **State Machines** - Set up policy lifecycle states
5. **Event Handlers** - Configure event triggers
6. **Validation Rules** - Enable invariant checking

### Schema Integration

**Steps:**
1. Upload `policies.jsonld` to Context Studio
2. Validate JSON-LD structure
3. Verify all 8 policy entities are recognized
4. Confirm supporting entities (CloudResource, PolicyViolation, etc.)
5. Test entity relationships
6. Validate state machines

### Policy Markdown Integration

**Link Policy Files:**
1. `resource-policy.md` → ResourcePolicy entity
2. `cost-trends-policy.md` → CostTrendsPolicy entity
3. `anomaly-policy.md` → AnomalyPolicy entity
4. `new-resource-policy.md` → NewResourcePolicy entity
5. `idle-resource-policy.md` → IdleResourcePolicy entity
6. `compliance-policy.md` → CompliancePolicy entity
7. `expensive-resource-policy.md` → ExpensiveResourcePolicy entity
8. `budget-policy.md` → BudgetPolicy entity

### AI Agent Configuration

**Enable AI Understanding:**
- Semantic reasoning over policy relationships
- State machine navigation
- Invariant validation
- Event-driven workflows
- Compliance checking
- Anomaly detection

## Technical Requirements

- **Context Studio Version:** Latest
- **JSON-LD Support:** Required
- **Markdown Rendering:** Required
- **Entity Linking:** Required
- **State Machine Support:** Required
- **Event System:** Required

## Setup Steps

### Step 1: Import JSON-LD Schema
```bash
# Upload schema to Context Studio
context-studio import schema/policies.jsonld
```

### Step 2: Link Policy Markdown Files
```bash
# Link each policy file to its entity
context-studio link-policy resource-policy.md ResourcePolicy
context-studio link-policy cost-trends-policy.md CostTrendsPolicy
context-studio link-policy anomaly-policy.md AnomalyPolicy
context-studio link-policy new-resource-policy.md NewResourcePolicy
context-studio link-policy idle-resource-policy.md IdleResourcePolicy
context-studio link-policy compliance-policy.md CompliancePolicy
context-studio link-policy expensive-resource-policy.md ExpensiveResourcePolicy
context-studio link-policy budget-policy.md BudgetPolicy
```

### Step 3: Validate Configuration
```bash
# Verify all entities are loaded
context-studio validate-entities

# Test entity relationships
context-studio test-relationships

# Verify state machines
context-studio test-states
```

### Step 4: Enable AI Agents
```bash
# Configure AI agent access
context-studio enable-ai-agents

# Test semantic reasoning
context-studio test-reasoning
```

## Validation Checklist

- [ ] JSON-LD schema imported successfully
- [ ] All 8 policy entities recognized
- [ ] Supporting entities loaded (CloudResource, PolicyViolation, etc.)
- [ ] Operations defined (ApplyPolicy, DetectViolation, etc.)
- [ ] States configured (PolicyDraft, PolicyActive, etc.)
- [ ] Policy markdown files linked to entities
- [ ] Entity relationships validated
- [ ] State machines functional
- [ ] Invariants enforced
- [ ] Events triggering correctly
- [ ] AI agents can query policies
- [ ] Semantic reasoning working

## Expected Outcome

A fully configured Context Studio environment where:
- AI agents understand all 8 policies
- Semantic relationships are navigable
- State machines enforce policy lifecycles
- Invariants validate business rules
- Events trigger appropriate actions
- Compliance checking is automated

## Result

Bob successfully created a comprehensive setup guide with:
- ✅ Step-by-step Context Studio configuration
- ✅ JSON-LD schema import instructions
- ✅ Policy markdown linking process
- ✅ AI agent configuration
- ✅ Validation checklist
- ✅ Troubleshooting tips

**Guide Created:** Context Studio setup documentation

## Key Features

- **Complete Setup:** End-to-end configuration guide
- **Validation:** Comprehensive validation checklist
- **AI-Ready:** Enables AI agent understanding
- **Production-Ready:** Enterprise-grade setup process
- **Troubleshooting:** Common issues and solutions

## Integration with ICA

Context Studio integrates with ICA (Intelligent Cloud Assistant) to:
- Provide semantic context to AI agents
- Enable policy-aware decision making
- Support compliance automation
- Enable cost optimization recommendations
- Facilitate multi-cloud governance

---

**Prompt Date:** 2026-05-19  
**Bob Version:** Advanced Mode  
**Outcome:** ✅ Success - Complete Context Studio setup guide