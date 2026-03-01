function deleteSelectedOAuthClients(_event) {
  let clientIDs = $("input[data-client-id]:checked").map(function () {
    return $(this).data("client-id");
  });
  let target = clientIDs.length === 1 ? "client" : "clients";

  CTFd.ui.ezq.ezQuery({
    title: "Delete clients",
    body: `Are you sure you want to delete ${clientIDs.length} ${target}?`,
    success: function () {
      CTFd.fetch(`/admin/sso/client/delete`, {
        method: "POST",
        body: JSON.stringify({
          client_ids: Array.from(clientIDs).join(","),
        }),
      }).then(() => {
        window.location.reload();
      });
    },
  });
}

function submitDiscovery() {
  const url = document.getElementById("discovery-url-input").value.trim();

  if (!url) {
    window.location.href = "/admin/sso/client/create";
    return;
  }

  function showDiscoveryError(message) {
    const errorEl = document.getElementById("discovery-error");
    errorEl.textContent = message;
    errorEl.classList.remove("d-none");
  }

  document.getElementById("discovery-error").classList.add("d-none");

  CTFd.fetch("/admin/sso/client/discover", {
    method: "POST",
    body: JSON.stringify({ url }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        showDiscoveryError(data.error);
        return;
      }
      const params = new URLSearchParams({
        authorize_url: data.authorize_url || "",
        access_token_url: data.access_token_url || "",
        user_info_url: data.user_info_url || "",
      });
      window.location.href = `/admin/sso/client/create?${params}`;
    })
    .catch(() => {
      showDiscoveryError("Failed to fetch discovery document.");
    });
}

$(() => {
  $("#oauth-clients-delete-button").click(deleteSelectedOAuthClients);
  $("#discovery-submit-btn").click(submitDiscovery);
  $("#discovery-modal").on("show.bs.modal", function () {
    document.getElementById("discovery-url-input").value = "";
    document.getElementById("discovery-error").classList.add("d-none");
  });
});
