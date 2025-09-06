<script setup>
import { ref } from 'vue'

const api = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const file = ref(null)
const query = ref('')
const answer = ref('')
const sources = ref([])

async function upload() {
  const fd = new FormData()
  fd.append('file', file.value.files[0])

  const r = await fetch(`${api}/upload`, { 
    method: 'POST', 
    body: fd 
  })
  const data = await r.json()
  alert(`Ingested chunks: ${data.chunks}`)
}

async function ask() {
  const r = await fetch(`${api}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: query.value, top_k: 4 })
  })
  const data = await r.json()
  answer.value = data.answer
  sources.value = data.sources
}
</script>

<template>
  <main class="p-6 max-w-3xl mx-auto">
    <h1>📚 Mini-RAG</h1>

    <section>
      <h3>Upload PDF</h3>
      <input type="file" ref="file" accept="application/pdf" />
      <button @click="upload">Upload & Ingest</button>
    </section>

    <section>
      <h3>Ask</h3>
      <input 
        v-model="query" 
        placeholder="Ask a question..." 
        style="width:100%" 
      />
      <button @click="ask">Ask</button>

      <pre style="white-space: pre-wrap">{{ answer }}</pre>
      <ul>
        <li 
          v-for="(s, i) in sources" 
          :key="i"
        >
          p.{{ s.page }} (score {{ s.score.toFixed(3) }})
        </li>
      </ul>
    </section>
  </main>
</template>

<style>
main { 
  font-family: ui-sans-serif, system-ui; 
}

button { 
  margin-top: 8px; 
}

section { 
  margin: 24px 0; 
}
</style>
