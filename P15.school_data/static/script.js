const stButtonEl = document.querySelector('.js-student-button');
const staffButtonEl = document.querySelector('.js-staff-button');

const stuLoginEl = document.querySelector('.js-login');

console.log("Script running");

stButtonEl.addEventListener('click', () => {
    console.log('HEYY');
    if (!stButtonEl.classList.contains("selected-button")) {
        stButtonEl.classList.add('selected-button');
        staffButtonEl.classList.remove('selected-button');

        let stHTML = `<p>Enter Student ID</p><form action="/student" method="POST">
                <input class='input-box' type="text" placeholder="ID" name="student-id">
                <button class='submit-button' type="submit">Submit</button>
            </form>`;
        stuLoginEl.innerHTML = stHTML;
    }


    })

staffButtonEl.addEventListener('click', () => {
    console.log('HEYY');
    if (!staffButtonEl.classList.contains("selected-button")) {
        staffButtonEl.classList.add('selected-button');
        stButtonEl.classList.remove('selected-button');
        stuLoginEl.innerHTML = '';

        let staffHTML = `<p>Enter Staff ID</p><form action="/staff" method="POST">
                <input class='input-box' type="text" placeholder="ID" name="staff-id"><br>
                <input class='input-box' type="password" placeholder="Password" name="staff-pass">
                <button class='submit-button' type="submit">Submit</button>
            </form>`;
        stuLoginEl.innerHTML = staffHTML;
        
    }

    })