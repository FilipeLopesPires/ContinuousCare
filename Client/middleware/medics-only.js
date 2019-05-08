export default function (context) {
    if(context.store.getters.isClient) {
        context.redirect("/");
    }
}