document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-card");
  const hidden = document.getElementById("interestsHidden");
  if (hidden) {
    const sync = () => {
      hidden.value = Array.from(document.querySelectorAll('input[name="interest_choice"]:checked'))
        .map(input => input.value).join(",");
    };
    document.querySelectorAll('input[name="interest_choice"]').forEach(input => input.addEventListener("change", sync));
    if (form) form.addEventListener("submit", sync);
    sync();
  }
  document.querySelectorAll('input[type="date"][name="travel_date"]').forEach(input => {
    const now = new Date();
    const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    input.min = local;
  });
});
