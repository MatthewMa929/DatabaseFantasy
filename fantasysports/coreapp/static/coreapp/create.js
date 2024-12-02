document.getElementById('table-select').addEventListener('change', function() {
    const selectedTable = this.value;
    const fieldsContainer = document.getElementById('fields-container');
    fieldsContainer.innerHTML = '';

    let fields = [];

    switch (selectedTable) {
        case 'criminals':
            fields = [
                { name: 'Criminal_ID', type: 'number', required: true },
                { name: 'Violent_Stat', type: 'checkbox', required: false, default: false },
                { name: 'Probation_Stat', type: 'checkbox', required: false, default: false },
                { name: 'Name', type: 'text', required: true, maxLength: 255 }
            ];
            break;
        case 'crimes':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Criminal_ID', type: 'number', required: true },
                { name: 'Crime_Code', type: 'text', required: true, maxLength: 30 },
                { name: 'Classification', type: 'text', required: true, maxLength: 30 }
            ];
            break;
        case 'charges':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Charge_Status', type: 'datetime-local', required: false },
                { name: 'Charge_Date', type: 'datetime-local', required: false }
            ];
            break;
        case 'sentencing':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Start_Date', type: 'datetime-local', required: false },
                { name: 'End_Date', type: 'datetime-local', required: false },
                { name: 'Violation_Num', type: 'number', required: false },
                { name: 'Sentence_Type', type: 'text', required: false, maxLength: 30 }
            ];
            break;
        case 'criminal_phone':
            fields = [
                { name: 'Criminal_ID', type: 'number', required: true },
                { name: 'Number', type: 'text', required: true, maxLength: 10 }
            ];
            break;
        case 'aliases':
            fields = [
                { name: 'Criminal_ID', type: 'number', required: true },
                { name: 'Alias', type: 'text', required: true, maxLength: 255 }
            ];
            break;
        case 'address':
            fields = [
                { name: 'Criminal_ID', type: 'number', required: true },
                { name: 'Addr', type: 'text', required: false, maxLength: 255 },
                { name: 'City', type: 'text', required: false, maxLength: 255 },
                { name: 'State', type: 'text', required: false, maxLength: 2 },
                { name: 'Zip_Code', type: 'text', required: false, maxLength: 5 }
            ];
            break;
        case 'hearing':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Hearing_Date', type: 'datetime-local', required: true },
                { name: 'Appeal_Cutoff_Date', type: 'datetime-local', required: false }
            ];
            break;
        case 'monetary':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Amount_Fined', type: 'number', required: false, step: '0.01' },
                { name: 'Amount_Paid', type: 'number', required: false, step: '0.01' },
                { name: 'Court_Fee', type: 'number', required: false, step: '0.01' },
                { name: 'Due_Date', type: 'datetime-local', required: false }
            ];
            break;
        case 'appeals':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Filing_Date', type: 'datetime-local', required: true },
                { name: 'Hearing_Date', type: 'datetime-local', required: false },
                { name: 'Appeal_Status', type: 'text', required: false, maxLength: 30 }
            ];
            break;
        case 'arresting_officers':
            fields = [
                { name: 'Crime_ID', type: 'number', required: true },
                { name: 'Badge_ID', type: 'number', required: true }
            ];
            break;
        case 'officer':
            fields = [
                { name: 'Badge_Number', type: 'number', required: true },
                { name: 'Name', type: 'text', required: false, maxLength: 255 },
                { name: 'Precinct', type: 'text', required: false, maxLength: 100 },
                { name: 'Officer_Status', type: 'text', required: false, maxLength: 100 }
            ];
            break;
        case 'officer_phone':
            fields = [
                { name: 'Badge_Number', type: 'number', required: true },
                { name: 'Number', type: 'text', required: true, maxLength: 10 }
            ];
            break;
    }

    fields.forEach(function(field) {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';

        const label = document.createElement('label');
        label.setAttribute('for', field.name);
        label.textContent = field.name.replace(/_/g, ' ') + ':';

        let input;
        if (field.type === 'checkbox') {
            input = document.createElement('input');
            input.type = 'checkbox';
            input.id = field.name;
            input.name = field.name;
            input.checked = field.default;
        } else {
            input = document.createElement('input');
            input.type = field.type;
            input.id = field.name;
            input.name = field.name;
            input.required = field.required;
            if (field.maxLength) {
                input.maxLength = field.maxLength;
            }
            if (field.step) {
                input.step = field.step;
            }
            
            // Add placeholder based on the field name
            input.placeholder = getPlaceholderText(field.name);
        
        }

        formGroup.appendChild(label);
        formGroup.appendChild(input);
        fieldsContainer.appendChild(formGroup);
    });
});

function getPlaceholderText(fieldName) {
    switch (fieldName) {
        case 'Criminal_ID':
        case 'Crime_ID':
        case 'Badge_Number':
            return 'Enter a numeric ID';
        case 'Name':
            return 'Enter the full name';
        case 'Number':
            return 'Enter a phone number';
        case 'Alias':
            return 'Enter an alias';
        case 'Addr':
            return 'Enter the street address';
        case 'City':
            return 'Enter the city';
        case 'State':
            return 'Enter the state abbreviation';
        case 'Zip_Code':
            return 'Enter the zip code';
        case 'Crime_Code':
        case 'Classification':
        case 'Sentence_Type':
        case 'Appeal_Status':
        case 'Precinct':
        case 'Officer_Status':
            return 'Enter a description';
        case 'Amount_Fined':
        case 'Amount_Paid':
        case 'Court_Fee':
            return 'Enter the amount';
        default:
            return '';
    }
}

document.getElementById('create-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const form = event.target;
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(function(field) {
        if (!field.value) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    if (isValid) {
        form.submit();
    }
});