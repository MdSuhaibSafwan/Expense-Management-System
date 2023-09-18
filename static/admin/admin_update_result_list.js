document.addEventListener("DOMContentLoaded", function(){
    var resList = document.getElementById("result_list");
    if (resList == null){
        return null;
    }
    var tBody = resList.getElementsByTagName("tbody")[0];
    var trs = tBody.getElementsByTagName("tr");
    var sum = 0;

    var promise = new Promise(function(resolve, reject){
        for (var tr of trs){
            var secPromise = new Promise(function(resolve, reject){
                let cost = tr.getElementsByClassName("field-cost")[0].textContent;
                let quantity = tr.getElementsByClassName("field-quantity")[0].textContent;
                let total = cost * quantity;
                sum += total
                return sum;
            })
        };
        resolve(sum);
    })
    .then(function(value){
        let tr = document.createElement("tr");
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        var td3 = document.createElement("td");
        var td4 = document.createElement("td");
        var td5 = document.createElement("td");
        td5.textContent = `${value}/-`;
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tBody.appendChild(tr);
        console.log(value);
    })
    
});