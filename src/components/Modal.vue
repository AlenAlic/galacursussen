<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div
          class="modal-container"
          :class="{
            'modal-large': size === 'large',
            'modal-medium': size === 'medium'
          }"
        >
          <div class="modal-header" v-if="title">
            <h4>{{ title }}</h4>
          </div>
          <div class="modal-body">
            <slot name="body"></slot>
          </div>
          <div class="modal-footer right-align">
            <slot name="button"></slot>
            <button v-if="closeBtn" class="modal-close-btn btn cancel" @click="$emit('close')">
              {{ closeBtn }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Modal",
  props: {
    title: String,
    closeBtn: String,
    size: String
  },
  data: function() {
    return {
      showModal: false
    };
  }
};
</script>

<style scoped lang="scss">
@import "../assets/css/config";
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  transition: opacity $transition-time ease;
  overflow-y: auto;
}
.modal-wrapper {
  margin: 96px 0;
}
.modal-container {
  width: 90%;
  max-width: 300px;
  margin: 0 auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all $transition-time ease;
  &.modal-large {
    max-width: 1000px;
  }
  &.modal-medium {
    max-width: 700px;
  }
  height: 90%;
  overflow-y: auto;
}
.modal-header h3 {
  margin-top: 0;
  color: $secondary-color;
}
.modal-body {
  margin: 20px 0;
}
.modal-close-btn {
  margin-left: 1rem;
}
.modal-enter {
  opacity: 0;
}
.modal-leave-active {
  opacity: 0;
}
.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
