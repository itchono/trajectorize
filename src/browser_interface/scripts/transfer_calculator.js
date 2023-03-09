function calculate_transfer() {
  // Get the values from the form
  var origin_body = document.getElementById("origin_body").value;
  var destination_body = document.getElementById("destination_body").value;
  var departure_time = document.getElementById("departure_time").value;
  var parking_orbit = document.getElementById("parking_orbit").value;
  var include_capture = document.getElementById("include_capture").value;
  var capture_orbit = document.getElementById("capture_orbit").value;

  var result = Module.ccall(
    "calculate_transfer",
    "number",
    [
      "number",
      "number",
      "number",
      "number",
      "number",
      "number",
      "number",
      "number",
    ],
    [
      departure_time,
      origin_body,
      destination_body,
      100,
      100,
      parking_orbit,
      capture_orbit,
      include_capture,
    ]
  );
}
