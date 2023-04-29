<template>
  <AppBar></AppBar>
    <div class="chat-container">
      <div class="chat-container__messages">
        <div v-for="chat in chats" :key="chat.message" :class="chat.role">
          <div class="message">
            <div class="message__text">{{chat.message}}</div>
          </div>
        </div>
      </div>
      <div class="chat-container__input">
        <textarea wrap="soft" placeholder="Type a message" v-model="messageText" @submit="test" @change="messageFinished = false" @focus="inputFocus" ref="chatInput"></textarea>
      </div>
    </div>
  <LoadingAnimation v-if="messageSending" color="#7d2ec8" size="60" class="ml-5 mt-n5"></LoadingAnimation>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import AppBar from "@/components/AppBar.vue";
import LoadingAnimation from "@/components/icons/LoadingAnimation.vue";
import * as events from "events";

const chats = ref([{
  role: "assistant",
  message: "Hello, I'm Friday. How can I help you today?",
}
])
const messageText = ref("");
//Use this to disable the event listener to prevent spamming callbacks
const messageSending = ref(false);
window.addEventListener('keydown', async (e) =>{
  console.log(e)
  if (e.key === 'Enter') {
    if(messageSending.value) return;

    messageSending.value = true;
    chats.value.push({
      role: "user",
      message: messageText.value,
    })
    messageText.value = "";
    e.target.blur();

    await sendMessage();
    messageSending.value = false;
  }
})
async function sendMessage() {
  console.log("Sending message...")
  try{
    const response = await fetch(`/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "chat-history": chats.value,
      }),
    });
    console.log("Response received")
    const data = await response.json();
    console.log(data)
    chats.value.push({
      role: "assistant",
      message: data.message,
    })
  }catch(err){
    console.log(err)
    chats.value.push({
      role: "assistant",
      message: "Your message could not be sent. Please try again later.",
    })
  }
}
function inputFocus(event: any){
  // event.target.blur();
}
</script>
<style lang="scss">
@use "@/styles/settings.scss" as *;
.chat-container{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: $white;
  padding: 10px;
  padding-top: 60px;
  overflow: hidden;
}
.chat-container__messages{
  width: 100%;
  overflow-y: scroll;
  padding: 10px;
  .user{
    display: flex;
    justify-content: flex-start;
    .message{
      background-color: $gray;
      border-radius: 10px 10px 0 10px;
      margin-left: auto;
      .message__text{
        padding: 10px;
      }
    }
  }
  .assistant{
    display: flex;
    justify-content: flex-end;
    .message{
      background-color: $purple;
      border-radius: 10px 10px 10px 0;
      margin-right:auto;
      .message__text{
        padding: 10px;
        color: $white;
      }
    }
  }
}
.chat-container__input{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  -webkit-backface-visibility: hidden;
  position: fixed;
  bottom:7px;
  left: 0;
  background-color: $white;
  textarea{
    width: 100%;
    border: none;
    border-radius: 10px;
    padding: 10px;
    padding-left: 15px;
    font-size: 19px;
    resize: none;
    &:focus{
      outline: none;
    }
  }
}
.message{
  margin-bottom: 10px;
}
</style>
