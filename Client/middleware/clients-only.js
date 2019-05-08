export default function (context) {
    if(context.store.getters.isMedic) {
        context.redirect("/patients");
    }
}