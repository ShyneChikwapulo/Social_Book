const fetchNews = async () => {
    console.log("Fetching news...");
    var url = '/api/news'; // Update the URL to point to your Django endpoint

    try {
        let response = await fetch(url);
        let data = await response.json(); // Call response.json() as a function
        console.log(data);

        let str = "";

        for (let item of data.articles) {
            str += `
                <div class="card my-4 bg-white shadow rounded-md  -mx-2 lg:mx-0" style="width: 33rem; height: 35rem; border-width: 2px; border-color:#fff;   ">
                    <div class="card-header" style="display: flex; align-items: center;">
                        <div class="profile-photo" style="margin-bottom:10px; margin-top:5px; margin-left:10px; ">
                            <img src="/static/assets/images/BBC.png" />
                        </div>
                        <div style=" margin-left: 15px; ">
                            <b><p> BBC News</p></b>
                        </div>
                      
                    </div>
                    <img src="${item.urlToImage}" class="card-img-top" alt="...">
                    <div class="card-body">
                        <b><h5 class="card-title">${item.title}</h5></b>
                        <p class="card-text">${item.description}</p>
                    </div>
                    <div class="card-footer" style="text-align: right;">
                        <a href="${item.url}" target="_blank" class="btn btn-primary" style="background: deepskyblue; color:white;  margin-bottom:100px;">Read Article</a>
                    </div>
                </div>
            `;
        }
        document.querySelector(".card-content").innerHTML = str;
    } catch (error) {
        console.error('Error fetching news:', error);
    }
}
fetchNews();