<template>
  <div class="container">
    <h1>{{ pageName }}</h1>
  </div>
</template>

<script>
export default {
  props: {
    pageName: String 
  }
};
</script>