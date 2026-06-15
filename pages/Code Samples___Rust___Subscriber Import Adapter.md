title:: Code Samples/Rust/Subscriber Import Adapter
asset-code:: CSMP-RS01
public:: true

- A Rust implementation of the [[Singine]] subscriber import adapter interface, demonstrating the [[AI as a Tool (Human-Controlled AI)]] pattern: a deterministic, pure-function transformation with no AI autonomy.
- ## Source
	- Language: Rust 1.79+
	- Crate dependencies: `serde`, `serde_json`, `csv`, `chrono`
- ## Code
	- ```rust
	  //! subscriber_import_adapter.rs
	  //! Pure-function platform adapter: raw CSV row → canonical Subscriber.
	  //! No AI inference; deterministic transformation only.
	  
	  use chrono::{DateTime, Utc};
	  use serde::{Deserialize, Serialize};
	  use std::collections::HashMap;
	  
	  #[derive(Debug, Serialize, Deserialize, Clone)]
	  pub struct RawSubscriber {
	      pub email: String,
	      pub source_platform: String,
	      pub fields: HashMap<String, String>,
	  }
	  
	  #[derive(Debug, Serialize, Deserialize)]
	  pub struct Subscriber {
	      pub email: String,
	      pub source_platform: String,
	      pub opted_in: bool,
	      pub imported_at: DateTime<Utc>,
	      pub metadata: HashMap<String, String>,
	  }
	  
	  #[derive(Debug, Serialize, Deserialize)]
	  pub struct ImportResult {
	      pub imported: Vec<Subscriber>,
	      pub skipped: usize,
	      pub errors: Vec<String>,
	  }
	  
	  /// Normalise a raw subscriber row into the canonical Subscriber shape.
	  /// Returns None if the row is invalid (missing email, malformed opt-in).
	  pub fn normalise(raw: RawSubscriber) -> Option<Subscriber> {
	      let email = raw.email.trim().to_lowercase();
	      if email.is_empty() || !email.contains('@') {
	          return None;
	      }
	      let opted_in = raw
	          .fields
	          .get("subscribed")
	          .map(|v| matches!(v.to_lowercase().as_str(), "true" | "yes" | "1"))
	          .unwrap_or(false);
	  
	      Some(Subscriber {
	          email,
	          source_platform: raw.source_platform,
	          opted_in,
	          imported_at: Utc::now(),
	          metadata: raw.fields,
	      })
	  }
	  
	  /// Process a batch of raw rows, deduplicating by email.
	  pub fn import_batch(rows: Vec<RawSubscriber>) -> ImportResult {
	      let mut seen = std::collections::HashSet::new();
	      let mut imported = Vec::new();
	      let mut skipped = 0;
	      let mut errors = Vec::new();
	  
	      for row in rows {
	          match normalise(row) {
	              None => {
	                  skipped += 1;
	                  errors.push("Invalid or missing email".into());
	              }
	              Some(sub) => {
	                  if seen.insert(sub.email.clone()) {
	                      imported.push(sub);
	                  } else {
	                      skipped += 1; // duplicate
	                  }
	              }
	          }
	      }
	  
	      ImportResult { imported, skipped, errors }
	  }
	  
	  #[cfg(test)]
	  mod tests {
	      use super::*;
	  
	      #[test]
	      fn test_dedup() {
	          let rows = vec![
	              RawSubscriber { email: "a@b.com".into(), source_platform: "ghost".into(),
	                  fields: [("subscribed".into(), "true".into())].into() },
	              RawSubscriber { email: "A@B.COM".into(), source_platform: "ghost".into(),
	                  fields: [("subscribed".into(), "true".into())].into() },
	          ];
	          let result = import_batch(rows);
	          assert_eq!(result.imported.len(), 1);
	          assert_eq!(result.skipped, 1);
	      }
	  
	      #[test]
	      fn test_invalid_email() {
	          let rows = vec![
	              RawSubscriber { email: "not-an-email".into(), source_platform: "mailchimp".into(),
	                  fields: HashMap::new() },
	          ];
	          let result = import_batch(rows);
	          assert_eq!(result.imported.len(), 0);
	          assert_eq!(result.skipped, 1);
	      }
	  }
	  ```
- ## Notes
	- This adapter implements the `PlatformAdapter` interface from `~/ws/singine/src/import/types.ts`
	- Deduplication is by normalised email (lowercase-trimmed); dedup across platforms happens in the Singine `normalize.ts` layer, not here
- ## See Also
	- [[Singine]]
	- [[Code Samples/Python/Scenario Validator]]
	- [[Code Samples/Go/Pipeline Orchestrator]]
