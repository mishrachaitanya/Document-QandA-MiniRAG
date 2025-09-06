<template>
  <div>
    <h1>Mini-RAG Document Q&A</h1>
    <UploadForm />
    <AskForm />
  </div>
</template>

<script>
import UploadForm from './components/UploadForm.vue'
import AskForm from './components/AskForm.vue'

export default {
  components: { UploadForm, AskForm }
}
</script>
