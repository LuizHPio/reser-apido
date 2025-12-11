const socket = io();

socket.on("warning", (data) => {
  alert(data);
});
