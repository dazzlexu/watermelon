/**
 * this part is for the JS
 * By using the axios to get the data from the link
 * and built the three cards
 */
const url = "https://covid19.mathdro.id/api";
//this part is using axios.js a library for asynchronous request basing a Promise A+
axios.get(url).then(function (r) {
  let {
    data: { confirmed, recovered, deaths, lastUpdate },
  } = r;
  //create the card by chart.js
  lastUpdate = new Date(lastUpdate).toDateString();
  let e1 = document.getElementById("confirmed");
  let e2 = document.getElementById("recovered");
  let e3 = document.getElementById("deaths");
  let dates = document.getElementsByClassName("date");
  e1.innerHTML = confirmed.value;
  e2.innerHTML = recovered.value;
  e3.innerHTML = deaths.value;
  for (let i = 0; i < dates.length; i++) {
    dates[i].innerHTML = lastUpdate;
  }
});

let label = [];
let confirmedCases = [];
let deathCase = [];
const url1 = "https://covid19.mathdro.id/api";
//get the data from the link
axios.get(url1 + "/daily").then((r) => {
  let { data } = r;
  data.map((dailyData) => {
    label.push(dailyData.reportDate);
    confirmedCases.push(dailyData.confirmed.total);
    deathCase.push(dailyData.deaths.total);
  });
  //create the chart
  var myChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: label,
      datasets: [
        {
          label: "confirmed",
          data: confirmedCases,
          backgroundColor: "red",
          borderWidth: 1,
          fill: false,
        },
        {
          label: "death",
          data: deathCase,
          backgroundColor: "blue",
          borderWidth: 1,
          fill: false,
        },
      ],
    },
    options: {
      options: {
        responsive: false,
      },
      scales: {
        xAxes: [
          {
            ticks: {
              display: false, //this will remove only the label
            },
          },
        ],
      },
    },
  });
});
//get the select country and add it to link eg: https://covid19.mathdro.id/api/countries/Austrilia
let select = document.getElementById("select");
axios.get(url1 + "/countries").then((data) => {
  let countryList = [];
  let {
    data: { countries },
  } = data;
  countries.map((country) => {
    countryList.push(country.name);
  });
  for (let i of countryList) {
    let y = document.createElement("option");
    y.text = i;
    select.add(y);
  }
});
//add the data to the card
$(() => {
  let selectedCountry = undefined;
  $("select").change(() => {
    selectedCountry = $("select").val();
    axios.get(`${url}/countries/${selectedCountry}`).then((r) => {
      let { data } = r;
      let e1 = document.getElementById("confirmed");
      let e2 = document.getElementById("recovered");
      let e3 = document.getElementById("deaths");
      let dates = document.getElementsByClassName("date");
      e1.innerHTML = data.confirmed.value;
      e2.innerHTML = data.recovered.value;
      e3.innerHTML = data.deaths.value;
    });
  });
});
let ctx = document.getElementById("myChart").getContext("2d");

mapboxgl.accessToken =
  "pk.eyJ1Ijoiamluc2h1YWlmdSIsImEiOiJja252NTM5bm8wODh6Mm9veTV6ZXUxanZ4In0.s5mqaayUUZ-N1mUTARyUNA";
var map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/dark-v10",
  zoom: 1.5,
  center: [0, 20]
});
var marker = new mapboxgl.Marker({
    draggable:true
}).setLnglat([0,0]).addTo(mao)
