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

$(() => {
  $("#oauth-clients-delete-button").click(deleteSelectedOAuthClients);
});
