// Add these variables at the beginning of the file
const editModal = document.getElementById("edit-modal");
const editForm = document.getElementById("edit-form");
const closeBtn = document.getElementsByClassName("close")[0];
const saveBtn = document.getElementById("save-btn");

function openEditModal(table, record, event) {
    console.log('openEditModal called with:', table, record);

    // Clear previous form fields
    editForm.innerHTML = "";

    // Generate form fields based on the table and record
    Object.entries(record).forEach(([key, value]) => {
        const label = document.createElement("label");
        label.textContent = key;
        const input = document.createElement("input");
        input.type = "text";
        input.name = key;
        input.value = value;
        editForm.appendChild(label);
        editForm.appendChild(input);
    });

    // Set the table and record ID as data attributes on the form
    editForm.dataset.table = table;
    // Set the table and record ID as data attributes on the form
    if ('criminal_id' in record) {
        editForm.dataset.recordId = record.criminal_id;
    } else if ('crime_id' in record) {
        editForm.dataset.recordId = record.crime_id;
    } else {
        // Handle the case where neither ID is present, perhaps by logging an error or setting a default value
        console.error('No criminal_id or crime_id found in record:', record);
    }

    // Open the modal
    editModal.style.display = "block";
}



closeBtn.onclick = function () {
  editModal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == editModal) {
    editModal.style.display = "none";
  }
};

// Handle form submission
saveBtn.onclick = function () {
    const formData = new FormData(editForm);
    const table = editForm.dataset.table;
    const recordId = editForm.dataset.recordId;
  
    // Show confirmation dialog
    if (confirm("Are you sure you want to save the changes?")) {
      const jsonData = {
        table: table,
        record_id: recordId,
      };
  
      // Convert form data to JSON
      for (const [key, value] of formData.entries()) {
        jsonData[key] = value;
      }
  
      // Send the edited data to the server
      fetch("/edit-record/", {
        method: "POST",
        body: JSON.stringify(jsonData),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            editModal.style.display = "none";
            searchRecords();
          } else {
            console.error("Error editing record:", data.error);
          }
        })
        .catch((error) => {
          console.error("Error editing record:", error);
        });
    }
  };
function closeEditModal() {
    editModal.style.display = "none";
  }