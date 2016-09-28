import QtQuick 2.0

ListModel {
    ListElement {
        blockDisplayName: "Add"
        blockType: "Add"
        defaultInputs: [ListElement{ID:"input1";TYPE:"Int"},ListElement{ID:"input2";TYPE:"Int"}]
        defaultOutputs: [ListElement{ID:"output";TYPE:"Int"}]
        description: "This block adds all the inputs and give an output."
    }
    ListElement {
        blockDisplayName: "Subtract"
        blockType: "Sub"
        defaultInputs: [ListElement{ID:"input1";TYPE:"Int"},ListElement{ID:"input2";TYPE:"Int"}]
        defaultOutputs: [ListElement{ID:"output1";TYPE:"Int"},ListElement{ID:"output2";TYPE:"Int"}]
        description: "This block subtracts 2 inputs and gives the difference and the inverse."
    }
    ListElement {
        blockDisplayName: "Divide"
        blockType: "Div"
        defaultInputs: [ListElement{ID:"input1";TYPE:"Int"},ListElement{ID:"input2";TYPE:"Int"}]
        defaultOutputs: [ListElement{ID:"output1";TYPE:"Int"},ListElement{ID:"output2";TYPE:"Int"}]
        description: "This block divide 2 inputs and gives the result and the reciprocal."
    }
    ListElement {
        blockDisplayName: "Multiply"
        blockType: "Mul"
        defaultInputs: [ListElement{ID:"input1";TYPE:"Int"},ListElement{ID:"input2";TYPE:"Int"}]
        defaultOutputs: [ListElement{ID:"output";TYPE:"Int"}]
        description: "This block divide 2 inputs and gives the result and the reciprocal."
    }
    ListElement {
        blockDisplayName: "Podometer"
        blockType: "podometer"
        defaultInputs:[ListElement{ID:"accelData";TYPE:"Frame"}]
        defaultOutputs:[ListElement{ID:"stepNumber";TYPE:"Int"},ListElement{ID:"stepNumberChart";TYPE:"Int"},ListElement{ID:"stepNumberMoyenne";TYPE:"Int"},ListElement{ID:"stepNumberMin";TYPE:"Int"}]
        description: "The podometer does a lot of stuff."
    }
}
