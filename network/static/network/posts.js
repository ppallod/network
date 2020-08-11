function fun(x) {
    var post_id = x.dataset.id
    var act = x.dataset.action

    fetch('/like', {
        method: 'PUT',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": '{{ csrf_token }}',
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: post_id,
            flag: act
        })
    })

    .then(response => response.json())
    .then(result => {
        const total_likes = result['total_likes'];
        document.querySelector(`#likes_post_${post_id}`).innerHTML = total_likes

    });
    if (act === "like"){
        x.style.color = "red";
        x.dataset.action="dislike"
    }

    else {
        x.style.color = "black";
        x.dataset.action="like";
    }

  };

  function editpost(x) {
      
      const post_id = x.dataset.id;

      const text = document.getElementById(`post_text_${post_id}`);
      text.style.display = "None";

      const textarea = document.getElementById(`post_textarea_${post_id}`);
      textarea.style.display = "block";
      
      x.style.display = "None";

      const save = document.getElementById(`post_save_${post_id}`);
      save.style.display = "block";

      save.addEventListener('click', () =>{
          console.log(textarea.value)
          
          fetch('/editpost', {
            method: 'PUT',
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": '{{ csrf_token }}',
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                post_id: post_id,
                text: textarea.value
            })
        })

        .then(response => response.json())
        .then(result => {
            const edited = result['edited'];
            console.log(edited)    
        });
        
        text.innerHTML = textarea.value;
        text.style.display = "block";
        
        x.style.display = "block";
        
        textarea.style.display = "None";
        save.style.display = "None";

      });

  }
