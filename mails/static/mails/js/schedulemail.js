document.getElementById("show_specific_time").style.display = "none";
document.getElementById("show_daily").style.display = "none";
document.getElementById("show_weekly").style.display = "none";
document.getElementById("show_monthly").style.display = "none";

function chooseaction(value) {
  console.log("working....");
  if (value === "specific_time") {
    document.getElementById("show_specific_time").style.display = "table-row";
    document.getElementById("show_daily").style.display = "none";
    document.getElementById("show_weekly").style.display = "none";
    document.getElementById("show_monthly").style.display = "none";
  } else if (value === "daily") {
    document.getElementById("show_specific_time").style.display = "none";
    document.getElementById("show_daily").style.display = "table-row";
    document.getElementById("show_weekly").style.display = "none";
    document.getElementById("show_monthly").style.display = "none";
  } else if (value === "weekly") {
    document.getElementById("show_specific_time").style.display = "none";
    document.getElementById("show_daily").style.display = "none";
    document.getElementById("show_weekly").style.display = "table-row";
    document.getElementById("show_monthly").style.display = "none";
  } else if (value === "monthly") {
    document.getElementById("show_specific_time").style.display = "none";
    document.getElementById("show_daily").style.display = "none";
    document.getElementById("show_weekly").style.display = "none";
    document.getElementById("show_monthly").style.display = "table-row";
  } else {
    document.getElementById("show_specific_time").style.display = "none";
    document.getElementById("show_daily").style.display = "none";
    document.getElementById("show_weekly").style.display = "none";
    document.getElementById("show_monthly").style.display = "none";
  }
}
