<template>
    <modal
        style="background-color:rgb(0,0,0,0);"
        name="eventOptions"
        transition="nice-modal-fade"
        :width="100"
        height="auto"
        :delay="100"
        :pivot-y="height"
        :pivot-x="width"
        :scrollable="true"
        >
        <b-container @mouseleave="closeMe">
            <b-row class="list" v-for='opt in options' :key="opt.id" v-html="opt" @click="sendOpt(opt)">
            </b-row>
        </b-container>
    </modal>
</template>

<script>

export default {
    name: 'EventOptions',
    props:[
        "height",
        "width",
        "options"
    ],
    methods: {
        closeMe(){
            this.$modal.hide("eventOptions")
        },
        sendOpt(opt){
            this.$emit("option", opt)
        }
    },
}
</script>

<style scoped>
.list{
    border: 1px solid #eee;
    background: #fff;
    padding: 5px;
    margin-left:-15px;
    margin-right:-15px;
    color: #000000;
    font-size: 16px;
}
.list:hover {
    background: #3face4;
    color: #fff; 
}
</style>
