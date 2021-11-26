//decalring html elemnts
const imgDiv = document.querySelector('.profile-pic-div');
const img = documnet.querySelector('#photo');
const file = documnet.querySelector('#file');
const uploadBtn = documnet.querySelector('#uploadBtn');

//if user hovers on img div

imgDiv.addEventListener('mouseenter', function(){
    uploadBtn.style.display = "block"
});

//if we hover out from img div

imgDiv.addEventListener('mouseleave', function(){
    uploadBtn.style.display = "none"
});

//lets work for image showing funcitonality when we choose a new one to upload

file.addEventListener('change', function(){
    //this refers to the file
    const choosedFile = this.files[0];

    if (choosedFile) {
        const reader = new FileReader();

        reader.addEventListener('load', function()
        {
            img.setAttribute('src', reader.result);
        });
        reader.readAsDataURL(choosedFile);
    }
});


<div class = "profile-pic-div">
                    <img src="https://dummyimage.com/150x150/6c757d/dee2e6.jpg" id= "photo" alt="..." />
                    <input type = "file" id= "file">
                    <label for = "file" id = "uploadBtn">Choose Photo</label> 
                  </div>
                  <script src="static/app.js"></script>


                  .profile-pic-div
{
    height: 200px;
    width: 200px;
    position: absolute;
    top:50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    overflow: hidden;
    border: 1px solid grey;
    
}

#photo{
    height: 100%;
    width: 100%;
}

#file{
    display: none;
}

#uplaodBtn{
    height: 40px;
    width: 100%;
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    background: (0, 0, 0, 0.7);
    color:wheat;
    line-height: 30px;
    font-family: sans-serif;
    font-size: 15px;
    cursor: pointer;
    display: none;
    
}