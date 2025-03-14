<script>
export default{
  data() {
    return {
      steps: 0
    }
  },
  methods: {
    real_steps() {
      axios.get('http://localhost:5000/steps/2025-03-13').then(result => {
        console.log(result)
        this.steps = result.data.steps
      })
    }
  }
}
</script>

<template>
  <main>
    <button @click="real_steps">Steps are {{ steps }}</button>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
