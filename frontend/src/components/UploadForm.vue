<template>
  <div>
    <h2>Upload PDF</h2>
    <input type="file" @change="uploadFile" />
    <p v-if="docId">Uploaded doc ID: {{ docId }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return { docId: null }
  },
  methods: {
    async uploadFile(event) {
      const file = event.target.files[0]
      const formData = new FormData()
      formData.append('file', file)

      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      this.docId = data.doc_id
    }
  }
}
</script>


