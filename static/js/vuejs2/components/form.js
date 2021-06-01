Vue.component('input-field', {
    delimiters: ['[[', ']]'],
    template: `
            <div  class="form-group" v-if="fieldData !== undefined">
                <label class="control-label ">
                   [[fieldData.name]]
                    <span class="asteriskField" v-if="fieldData.required">*</span>
                </label>
                <div class="controls ">
                    <input
                            type="text"
                            class="textinput textInput form-control"
                            v-model="fieldData.value"
                            :disabled="fieldData.disabled"
                            :required="fieldData.required"
                            maxlength="30"
                    >
                </div>
            </div>
            `,
    props: {
        fieldData: {
            type: Object,
        },
    }
})


Vue.component('select-field', {
    delimiters: ['[[', ']]'],
    template: `
               <div class="form-group" v-if="fieldData !== undefined">
                    <label class="control-label ">
                        [[fieldData.name]]
                        <span class="asteriskField" v-if="fieldData.required">*</span>
                    </label>
                    <div class="controls ">
                        <select
                            v-bind="$attrs"
                            class="select form-control"
                            v-model="fieldData.value"
                            :disabled="fieldData.disabled"
                            :required="fieldData.required"
                            
                        >
                            <option
                                v-for="choice in fieldData.choices"
                                :value="choice.key"
                                :selected="choice.key === fieldData.value"
                                @change="selectedChoice"
                             
                            >
                              [[choice.name]]
                            </option>
                        </select>
                    </div>
                </div>
            `,
    props: {
        fieldData: {
            type: Object,
        },

    },
    methods: {
        selectedChoice(event) {
            this.fieldData.value = event.target.value;
        }
    }
})


Vue.component('radio-select-field', {
    delimiters: ['[[', ']]'],
    template: `
              <div class="form-group" v-if="fieldData !== undefined">
                <label class="control-label ">
                    [[fieldData.name]]
                    <span class="asteriskField" v-if="fieldData.required">*</span>
                </label>
                <div class="controls">
                <div class="row">
                <label class="radio" v-for="choice in fieldData.choices">
                    
                      <input
                          type="radio"
                          :name="fieldData.name"
                          :value="choice.key"
                          :checked="choice.key === fieldData.value"
                          @change="selectedChoice"
                        >
                        [[choice.name]]
                    
                   
                      
                    </label>
                </div>
                    
                </div>
            </div>
              
            `,
    props: {
        fieldData: {
            type: Object,

        },

    },
    methods: {
        selectedChoice(event) {
            this.fieldData.value = event.target.value;

        }
    }
})

