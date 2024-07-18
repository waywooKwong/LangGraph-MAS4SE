<template>
  <div class="image-generator">
    <h1>Image Generator</h1>
    <form @submit.prevent="generateImages">
      <div>
        <label for="prompt">Prompt:</label>
        <input type="text" v-model="prompt" id="prompt" required />
      </div>
      <div>
        <label for="numImages">Number of Images:</label>
        <input
          type="number"
          v-model="numImages"
          id="numImages"
          min="1"
          required
        />
      </div>
      <button type="submit">Generate Images</button>
    </form>
    <div v-if="imageUrls.length > 0" class="images">
      <h2>Generated Images</h2>
      <div v-for="(imageUrl, index) in imageUrls" :key="index">
        <img :src="imageUrl" :alt="'Generated Image ' + (index + 1)" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      prompt: "",
      numImages: 1,
      imageUrls: [],
    };
  },
  methods: {
    async generateImages() {
      try {
        const response = await fetch("http://localhost:8000/generate_image", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            prompt: this.prompt,
            numImages: this.numImages,
          }),
        });
        const data = await response.json();
        this.imageUrls = data.image_urls.map(
          (url) => `http://localhost:8000${url}`
        );
      } catch (error) {
        console.error("Error generating images:", error);
      }
    },
  },
};
</script>

<style scoped>
.image-generator {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

form {
  display: flex;
  flex-direction: column;
}

form > div {
  margin-bottom: 10px;
}

.images {
  margin-top: 20px;
}

.images img {
  max-width: 100%;
  height: auto;
  display: block;
  margin-bottom: 10px;
}
</style>
