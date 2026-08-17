use std::collections::HashMap;
use std::hash::Hash;

pub struct Grouped<K, V> {
    groups: HashMap<K, Vec<V>>,
}

impl<K, V> Grouped<K, V> {
    pub fn new() -> Self {
        Self {
            groups: HashMap::new(),
        }
    }

    /// Insert `value` into the group named `key`.
    pub fn insert(&mut self, key: K, value: V)
    where
        K: Eq + Hash,
    {
        self.groups.entry(key).or_default().push(value);
    }

    /// Insert `value`, deriving its group key from the value itself.
    pub fn insert_with<F>(&mut self, value: V, key_of: F)
    where
        K: Eq + Hash,
        F: FnOnce(&V) -> K,
    {
        let key = key_of(&value);
        self.insert(key, value);
    }

    /// Transform every value with `f`, producing a new Grouped with the same keys.
    pub fn map_values<U, F>(self, mut f: F) -> Grouped<K, U>
    where
        K: Eq + Hash,
        F: FnMut(V) -> U,
    {
        let mut groups = HashMap::new();
        for (k, vs) in self.groups {
            let mapped = vs.into_iter().map(&mut f).collect();
            groups.insert(k, mapped);
        }
        Grouped { groups }
    }

    /// Keep only the groups for which `keep` returns true.
    pub fn retain_groups<F>(&mut self, mut keep: F)
    where
        F: FnMut(&K, &[V]) -> bool,
    {
        self.groups.retain(|k, vs| keep(k, vs));
    }

    /// Consume into (key, values) pairs, sorted by key.
    pub fn into_sorted(self) -> Vec<(K, Vec<V>)>
    where
        K: Ord,
    {
        let mut v: Vec<_> = self.groups.into_iter().collect();
        v.sort_by(|a, b| a.0.cmp(&b.0));
        v
    }

    /// Total number of values across all groups.
    pub fn total(&self) -> usize {
        self.groups.values().map(|vs| vs.len()).sum()
    }
}
