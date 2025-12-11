socket.on("connect", () => {
  console.log("CONNECTED");
});

socket.on("disconnect", () => {
  console.log("DISCONNECTED");
});

socket.on("successful-reserve", (id, resourceType) => {
  updateResourceStatus(id, "Em Uso", resourceType);
});

socket.on("successful-unreserve", (id, resourceType) => {
  updateResourceStatus(id, "Disponível", resourceType);
});

let updateResourceStatus = (id, newStatus, resourceType) => {
  const resourceElement = document.querySelector(
    `.resource-list[data-type='${resourceType}'] .resource-item[data-id="${id}"]`
  );

  if (resourceElement) {
    const statusSpan = resourceElement.querySelector(".status");
    const reserveButton = resourceElement.querySelector(".btn");

    statusSpan.textContent = newStatus;
    statusSpan.classList.remove("available", "reserved");

    if (newStatus === "Reservada") {
      statusSpan.classList.add("reserved");
      if (reserveButton) {
        reserveButton.removeAttribute("disabled");
      }
    } else if (newStatus === "Disponível") {
      statusSpan.classList.add("available");
      if (reserveButton) {
        reserveButton.setAttribute("disabled", "");
      }
    }
  }
};
