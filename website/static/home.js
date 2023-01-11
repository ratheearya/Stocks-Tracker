function addStock(stock){
    fetch("/addStock", {
        method: "POST",
        body: JSON.stringify(stock),
    }).then((_res) => {
        window.location.href = "/";
      });
}

function deleteStock(stock_id){
    fetch("/deleteStock", {
        method: "POST",
        body: JSON.stringify({stock_id:stock_id}),
    }).then((_res) => {
        window.location.href = "/";
      });
}