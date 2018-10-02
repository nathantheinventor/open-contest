exports.curTimeString = _ => {
    let d = new Date();
    let month = d.getMonth() + 1;
    let day = d.getDate();
    let year = d.getFullYear();
    let hour = d.getHours();
    let min = d.getMinutes();
    let sec = d.getSeconds() + d.getMilliseconds() / 1000;
    return `${month}/${day}/${year} ${hour}:${min}:${sec}`;
}