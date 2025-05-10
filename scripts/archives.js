document.getElementById("scrape-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const year = document.getElementById("year-select").value;
  const event = document.getElementById("event-select").value;
  const conference = document.querySelector('input[name="conference"]:checked').value;
  const level = document.querySelector('input[name="level"]:checked').value;

  let district = 0, region = 0, state = 0;
  if (level === "district") district = document.getElementById("district-number").value;
  if (level === "region") region = document.getElementById("region-number").value;
  if (level === "state") state = document.getElementById("state-number").value;

  const params = { event, conference, district, region, state, year };
  
  const response = await fetch("/scrape", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });

  const blob = await response.blob();
  const a = document.createElement("a");
  a.href = window.URL.createObjectURL(blob);
  a.download = "results.zip";
  a.click();
});
