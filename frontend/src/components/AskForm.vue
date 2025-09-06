<template>
  <div>
    <h2>Ask a Question</h2>
    <input v-model="query" placeholder="Type your question" />
    <button @click="askQuestion">Ask</button>
    <p v-if="answer">Answer: {{ answer.answer }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return { query: '', answer: null }
  },
  methods: {
    async askQuestion() {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: this.query, top_k: 3 })
      })
      this.answer = await res.json()
    }
  }
}
</script>
