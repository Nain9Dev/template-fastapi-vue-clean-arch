<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Item {
  id: number;
  title: string;
  description: string;
  is_active: boolean;
  created_at: string;
}

interface Health {
  status: string;
  version: string;
  environment: string;
  database: string;
}

const health = ref<Health | null>(null);
const items = ref<Item[]>([]);
const newTitle = ref('');
const newDesc = ref('');
const isLoading = ref(false);
const errorMsg = ref('');

const fetchHealth = async () => {
  try {
    const res = await fetch('/api/v1/health');
    if (res.ok) {
      health.value = await res.json();
    }
  } catch {
    health.value = {
      status: 'offline',
      version: '1.0.0',
      environment: 'local',
      database: 'disconnected'
    };
  }
};

const fetchItems = async () => {
  try {
    const res = await fetch('/api/v1/items');
    if (res.ok) {
      items.value = await res.json();
    }
  } catch (err) {
    console.error('Failed to load items', err);
  }
};

const createItem = async () => {
  if (!newTitle.value.trim()) return;
  isLoading.value = true;
  errorMsg.value = '';

  try {
    const res = await fetch('/api/v1/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: newTitle.value,
        description: newDesc.value
      })
    });

    if (!res.ok) {
      const err = await res.json();
      errorMsg.value = err.detail?.detail || 'Validation error';
      return;
    }

    newTitle.value = '';
    newDesc.value = '';
    await fetchItems();
  } catch (err) {
    errorMsg.value = String(err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await fetchHealth();
  await fetchItems();
});
</script>

<template>
  <div class="shell">
    <header class="hero">
      <div class="container">
        <div class="badge-row">
          <span class="badge" :class="health?.status === 'operational' ? 'badge-good' : 'badge-warn'">
            API: {{ health?.status || 'connecting...' }}
          </span>
          <span class="badge badge-meta">PostgreSQL: {{ health?.database || 'ready' }}</span>
          <span class="badge badge-meta">Cost: 0,00 €</span>
        </div>
        <h1 class="title">FastAPI + Vue 3 Clean Architecture</h1>
        <p class="subtitle">
          Production template with tactical domain modeling, async database repositories, strict Pydantic v2 validation, and TypeScript client.
        </p>
      </div>
    </header>

    <main class="container content">
      <section class="card create-card">
        <h2>Create Item (Domain Invariant Test)</h2>
        <form @submit.prevent="createItem" class="form">
          <div class="form-group">
            <label for="title">Title (min. 3 characters)</label>
            <input id="title" v-model="newTitle" placeholder="e.g. Audit Log Worker" required />
          </div>
          <div class="form-group">
            <label for="desc">Description</label>
            <input id="desc" v-model="newDesc" placeholder="e.g. Asynchronous telemetry pipeline" />
          </div>
          <button type="submit" :disabled="isLoading" class="btn-submit">
            {{ isLoading ? 'Submitting...' : 'Save Item' }}
          </button>
        </form>
        <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      </section>

      <section class="card list-card">
        <div class="list-header">
          <h2>Persisted Items ({{ items.length }})</h2>
          <button @click="fetchItems" class="btn-refresh">Refresh</button>
        </div>

        <div v-if="items.length === 0" class="empty">
          No items created yet. Add one above to test the async PostgreSQL pipeline.
        </div>

        <div v-else class="items-grid">
          <div v-for="item in items" :key="item.id" class="item-card">
            <div class="item-header">
              <span class="item-title">{{ item.title }}</span>
              <span class="item-id">#{{ item.id }}</span>
            </div>
            <p class="item-desc">{{ item.description || 'No description provided' }}</p>
            <span class="item-date">{{ new Date(item.created_at).toLocaleTimeString() }}</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style>
:root {
  --bg: #090c15;
  --surface: #101524;
  --surface-hover: #161c2e;
  --border: rgba(255, 255, 255, 0.08);
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --accent: #38bdf8;
  --green: #22c55e;
  --red: #ef4444;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  padding-top: 38px;
  line-height: 1.5;
}

.shell { min-height: 100vh; }
.container { max-width: 960px; margin: 0 auto; padding: 0 20px; }

.hero {
  padding: 48px 0 32px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(56, 189, 248, 0.04) 0%, transparent 100%);
}

.badge-row { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
.badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 9999px;
  font-family: var(--font-mono);
}
.badge-good { background: rgba(34, 197, 94, 0.15); color: var(--green); border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-warn { background: rgba(239, 68, 68, 0.15); color: var(--red); border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-meta { background: rgba(255, 255, 255, 0.06); color: var(--text-muted); border: 1px solid var(--border); }

.title { font-size: 32px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 10px; }
.subtitle { font-size: 15px; color: var(--text-muted); max-width: 640px; }

.content { padding-top: 36px; display: flex; flex-direction: column; gap: 28px; padding-bottom: 60px; }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
}
.card h2 { font-size: 16px; font-weight: 700; margin-bottom: 16px; }

.form { display: grid; grid-template-columns: 1fr 1fr auto; gap: 14px; align-items: end; }
@media (max-width: 720px) {
  .form { grid-template-columns: 1fr; }
}

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12px; color: var(--text-muted); font-weight: 500; }
.form-group input {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  color: #fff;
  font-family: inherit;
  font-size: 14px;
}
.form-group input:focus { outline: 2px solid var(--accent); border-color: transparent; }

.btn-submit, .btn-refresh {
  background: var(--accent);
  color: #040914;
  border: none;
  border-radius: 6px;
  padding: 9px 16px;
  font-weight: 600;
  cursor: pointer;
  font-size: 13px;
  transition: opacity 0.15s;
}
.btn-submit:hover, .btn-refresh:hover { opacity: 0.9; }

.btn-refresh {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text);
  border: 1px solid var(--border);
}

.error { color: var(--red); font-size: 13px; margin-top: 10px; }

.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.items-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
.item-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.item-header { display: flex; justify-content: space-between; }
.item-title { font-weight: 600; font-size: 14px; color: #fff; }
.item-id { font-size: 11px; font-family: var(--font-mono); color: var(--accent); }
.item-desc { font-size: 12px; color: var(--text-muted); flex-grow: 1; }
.item-date { font-size: 10px; color: var(--text-muted); font-family: var(--font-mono); }
.empty { font-size: 13px; color: var(--text-muted); padding: 24px 0; text-align: center; }
</style>
