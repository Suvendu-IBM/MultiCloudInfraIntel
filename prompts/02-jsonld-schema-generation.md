# Prompt: Generate JSON-LD Schema for Context Studio

## Context
This prompt was used to generate the JSON-LD schema file that defines the semantic model for all 8 policies in Context Studio. The schema enables AI agents to understand policy relationships, states, and operations.

## Original Prompt to Bob

Bob, create a comprehensive JSON-LD schema file for Context Studio that models all 8 policies as semantic entities with states, operations, and relationships.

## Schema Requirements

### 8 Policy Entities to Model

1. **ResourcePolicy** - Base policy for resource management
2. **CostTrendsPolicy** - Cost trend monitoring
3. **AnomalyPolicy** - Anomaly detection (20% threshold, 7-day baseline)
4. **NewResourcePolicy** - New resource tracking
5. **IdleResourcePolicy** - Idle resource detection (CPU <5%, 14 days)
6. **CompliancePolicy** - Compliance enforcement (required tags: owner, cost-center, environment)
7. **ExpensiveResourcePolicy** - Expensive resource monitoring (limit: 10)
8. **BudgetPolicy** - Budget management (warning: 80%, critical: 100%)

### Schema Structure

Each policy entity must include:
- **Identity Key:** Unique identifier (policyId: UUID)
- **Human Reference:** Human-readable name (policyName)
- **Attributes:** Policy-specific configuration
- **Invariants:** Business rules and constraints
- **States:** Policy lifecycle states (Draft, Active, Suspended, Archived)
- **Initial State:** Starting state (PolicyDraft)
- **Terminal States:** End states (PolicyArchived)
- **Relationships:** Links to other entities (CloudResource, PolicyViolation, AlertNotification)
- **Events:** Events emitted by the policy

### Supporting Entities

- **CloudResource** - Cloud infrastructure resources
- **PolicyViolation** - Violation records
- **AlertNotification** - Alert notifications
- **CostReport** - Cost analysis reports

### Operations

- **ApplyPolicy** - Apply policy to resources
- **DetectViolation** - Detect policy violations
- **SendAlert** - Send alert notifications
- **GenerateReport** - Generate cost reports

### States

- **Policy States:** Draft, Active, Suspended, Archived
- **Violation States:** Open, Acknowledged, Resolved, Ignored

## Technical Requirements

- **Format:** JSON-LD (Linked Data)
- **Context:** SRO (Semantic Resource Ontology) namespace
- **Schema.org:** Integration for standard properties
- **Validation:** All entities must have identity keys and human references
- **Relationships:** Explicit links between entities using @id and @type
- **Invariants:** Business rules encoded as constraints

## Expected Output

A complete `policies.jsonld` file with:
- @context definition with SRO and schema.org namespaces
- @graph containing all 8 policy entities
- Supporting entities (CloudResource, PolicyViolation, etc.)
- Operations (ApplyPolicy, DetectViolation, etc.)
- States (PolicyDraft, PolicyActive, etc.)
- Proper JSON-LD structure for Context Studio

## Result

Bob successfully generated a comprehensive JSON-LD schema with:
- ✅ All 8 policy entities with complete attributes
- ✅ Invariants encoding business rules (e.g., "cpuThreshold must be less than 5 percent")
- ✅ State machines for policy and violation lifecycles
- ✅ Operations with preconditions and postconditions
- ✅ Relationships between entities
- ✅ Events emitted by policies
- ✅ 623 lines of semantic model

**File Generated:** `schema/policies.jsonld` (623 lines)

## Key Features

- **Semantic Relationships:** Policies relate to CloudResource, PolicyViolation, AlertNotification
- **State Machines:** Clear lifecycle states for policies and violations
- **Business Rules:** Invariants like "warningThreshold must be 80 percent"
- **Event-Driven:** Policies emit events (PolicyActivated, PolicyViolated, etc.)
- **Context Studio Ready:** Fully compatible with ICA Context Studio

---

**Prompt Date:** 2026-05-18  
**Bob Version:** Advanced Mode  
**Outcome:** ✅ Success - Production-ready JSON-LD schema