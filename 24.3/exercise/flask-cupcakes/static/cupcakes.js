const BASE_URL = "http://localhost:5000/api";


/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
  return `
    <tr>
      <td class="align-middle text-center">
        <img class="cupcake-img rounded-circle" src="${cupcake.image}" alt="(no image provided)">
      </td>
      <td class="align-middle">${cupcake.flavor}</td>
      <td class="align-middle">${cupcake.size}</td>
      <td class="align-middle">${cupcake.rating}</td>
      <td class="align-middle">${cupcake.id}<img data-cupcake-id=${cupcake.id} class="delete-button delete-button-icon" src="/static/tenor.gif" title="Delete Flavor, PLEASE!!!"/></td>
    </tr>
  `;
}


/** put initial cupcakes on page. */

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcakes-list").append(newCupcake);
  }
}


/** handle form for adding of new cupcakes */

$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});


/** handle clicking delete: delete cupcake */

$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let cupcakeId = $(evt.target).attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $(evt.target).closest('tr').remove();
});


$(showInitialCupcakes);
