function buyGame(button) {
    const url = "/buy_game";
    const userId = button.getAttribute("data-user-id");
    const gameId = button.getAttribute("data-game-id");
    console.log(userId);
    console.log(gameId);
    fetch(url, {
        method: "post",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify({ userId: userId, gameId: gameId }),
    });
}